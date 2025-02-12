"use server";

import { stackServerApp } from "@/stack";
import { tinyshop } from "./api";

// Create a new team and shop
export const createNewTeam = async (displayName: string) => {
  // New team
  console.log("Creating new team : createNewTeam");
  const user = await stackServerApp.getUser({ or: "throw" });
  const newTeam = await stackServerApp.createTeam({
    displayName: displayName,
  });
  await newTeam.addUser(user.id);
  await user.setSelectedTeam(newTeam);

  console.log("Creating new team : createNewTeam: ", newTeam);

  try {
    await createDashboardKey();
    console.log("Post createDashboardKey");
    return newTeam.id;
  } catch (error) {
    console.error("Error creating dashboard, deleting team, error", error);
    await newTeam.delete();
    // TODO return error
  }
};

const createDashboardKey = async () => {
  console.log("inside createDashboardKey");
  const user = await stackServerApp.getUser({ or: "throw" });
  if (!user.selectedTeam?.id) return;

  console.log("inside createDashboardKey: ", user.selectedTeam);

  const data = await tinyshop.shops.create({
    livemode: false,
    name: user.selectedTeam.displayName,
    stack_auth_team_id: user.selectedTeam?.id,
    stack_auth_user_id: user.id,
  });

  console.log("createDashboardKey: data", data);
  // TODO Save the shop id to team
  const { shop_id, shop_handle, dashboard_key } = data;
  // Save the dashboard key user
  const newDashboardKeys = {
    ...(user.serverMetadata?.dashboardKeys || {}), // Safely access dashboardKeys
  };
  const newShopHandles = {
    ...(user.serverMetadata?.shopHandles || {}),
  };

  // TODO hash this?
  newDashboardKeys[user.selectedTeam.id] = dashboard_key;
  newShopHandles[user.selectedTeam.id] = shop_handle;

  await user.update({
    serverMetadata: {
      ...(user.serverMetadata || {}), // Safely include existing serverMetadata
      dashboardKeys: newDashboardKeys,
      shopHandles: newShopHandles,
    },
  });
};

// TODO if remove user from team, remove dashboardKey from serverMetadata
