"use server";

import { stackServerApp } from "@/stack";
import { tinyshop } from "./api";

// Create a new team and shop
export const createNewTeam = async (displayName: string) => {
  // New team
  const user = await stackServerApp.getUser({ or: "throw" });
  const newTeam = await stackServerApp.createTeam({
    displayName: displayName,
  });
  await newTeam.addUser(user.id);
  await user.setSelectedTeam(newTeam);

  try {
    await createDashboardKey();
  } catch (error) {
    await newTeam.delete();
    // TODO return error
  }
};

const createDashboardKey = async () => {
  const user = await stackServerApp.getUser({ or: "throw" });
  if (!user.selectedTeam?.id) return;

  const data = await tinyshop.shops.create({
    livemode: false,
    name: user.selectedTeam.displayName,
    stack_auth_team_id: user.selectedTeam?.id,
    stack_auth_user_id: user.id,
  });
  // TODO Save the shop id to team
  const { shop_id, dashboard_key } = data;
  // Save the dashboard key user
  const newDashboardKeys = {
    ...(user.serverMetadata?.dashboardKeys || {}), // Safely access dashboardKeys
  };

  // TODO hash this?
  newDashboardKeys[user.selectedTeam.id] = dashboard_key;

  await user.update({
    serverMetadata: {
      ...(user.serverMetadata || {}), // Safely include existing serverMetadata
      dashboardKeys: newDashboardKeys,
    },
  });
};

// TODO if remove user from team, remove dashboardKey from serverMetadata
