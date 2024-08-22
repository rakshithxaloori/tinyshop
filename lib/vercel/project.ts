"use server";
const VERCEL_AUTH_TOKEN = process.env.DASHBOARD_VERCEL_AUTH_TOKEN;
const VERCEL_TEAM_ID = process.env.DASHBOARD_VERCEL_TEAM_ID;

// TODO
type EnvVariable = {
  gitBranch?: string;
  key: string;
  target: string;
  type: string;
  value: string;
};

const ENV_VARIABLES = [
  {
    gitBranch: "main",
    key: "name", // TODO
    target: "[production]",
    type: "encrypted",
    value: "value", // TODO
  },
];

const GIT_REPO = "tinyshop-me/storefront";

export const createProject = async (handle: string,
  environment: Array<EnvVariable> = ENV_VARIABLES,
) => {
  const data = {
    name: handle,
    enableAffectedProjectsDeployments: true,
    environmentVariables: environment,
    framework: "nextjs",
    gitRepository: {
      repo: GIT_REPO,
      type: "github",
    },
    oidcTokenConfig: {
      enabled: true,
    },
  };
  const response = await fetch(
    `https://api.vercel.com/v10/projects?teamId=${VERCEL_TEAM_ID}`,
    {
      body: JSON.stringify(data),
      headers: {
        Authorization: `Bearer ${VERCEL_AUTH_TOKEN}`,
      },
      method: "post",
    }
  );
  const res_json = await response.json();
  console.log("RESPONSE createProject:", res_json);
};

export const addDomainToProject = async (handle: string) => {
  const data = {
    name: `${handle}.tinyshop.me`,
  };
  const response = await fetch(
    `https://api.vercel.com/v10/projects/${handle}/domains?teamId=${VERCEL_TEAM_ID}`,
    {
      body: JSON.stringify(data),
      headers: {
        Authorization: `Bearer ${VERCEL_AUTH_TOKEN}`,
      },
      method: "post",
    }
  );

  const res_json = await response.json();
  console.log("RESPONSE addDomainToProject:", res_json);
};

export const redeployProject = async (handle: string) => {
  const data = {
    name: handle,
    gitSource: {
      ref: "main",
      repoId: 820312336,
      type: "github",
    },
    projectSettings: {
      framework: "nextjs",
    },
    target: "production",
  };
  const response = await fetch(
    `https://api.vercel.com/v13/deployments?forceNew=0&skipAutoDetectionConfirmation=0&teamId=${VERCEL_TEAM_ID}`,
    {
      body: JSON.stringify(data),
      headers: {
        Authorization: `Bearer ${VERCEL_AUTH_TOKEN}`,
      },
      method: "post",
    }
  );
  const res_json = await response.json();
  console.log("RESPONSE redeployProject:", res_json);
};

export const getEnvVariables = async (handle: string) => {
  const response = await fetch(
    `https://api.vercel.com/v9/projects/${handle}/env?teamId=${VERCEL_TEAM_ID}`,
    {
      headers: {
        Authorization: `Bearer ${VERCEL_AUTH_TOKEN}`,
      },
    }
  );
  console.log("RESPONSE getEnvVariables:", response.headers);
  const res_json = await response.json();
  // console.log("RESPONSE getEnvVariables:", res_json);
  return res_json;
}

export const editEnvVariable = async (
  handle: string,
  name: string,
  value: string
) => {

  try {
    const envVar = await getEnvVariables(handle);
    // console.log("ENV VARIABLES:", envVar);
    const env = envVar.envs.find((env: any) => env.key === name);
    if (!env) {
      console.error("Env variable not found");
      return;
    }

    const envId = env.id;
    const data = {
      // gitBranch: "main",
      key: name,
      target: ["production"],
      type: "encrypted",
      value: value,
    };
    console.log("DATA editEnvVariable:", data);
    console.log("ENV ID:", envId);
    console.log("handle:", handle);
    console.log("vercel auth token:", VERCEL_AUTH_TOKEN);
    console.log("vercel team id:", VERCEL_TEAM_ID);
    console.log("url:", `https://api.vercel.com/v9/projects/${handle}/env/${envId}?teamId=${VERCEL_TEAM_ID}`);
    console.log("data:", JSON.stringify(data));

    const response = await fetch(
      `https://api.vercel.com/v9/projects/${handle}/env/${envId}?teamId=${VERCEL_TEAM_ID}`,
      {
        body: JSON.stringify(data),
        headers: {
          Authorization: `Bearer ${VERCEL_AUTH_TOKEN}`,
        },
        method: "patch",
      }
    );
    console.log("data ", response.status)
    console.log("data ", response.statusText)
    console.log("response", response)
    const res_json = await response.json();
    console.log("RESPONSE editEnvVariable:", res_json);
  }
  catch (e) {
    console.error("ERROR editEnvVariable:", e);
  }
};
