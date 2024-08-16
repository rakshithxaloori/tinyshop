const VERCEL_AUTH_TOKEN = process.env.VERCEL_AUTH_TOKEN;
const VERCEL_TEAM_ID = process.env.VERCEL_TEAM_ID;

// TODO
const ENV_VARIABLES = [];

const GIT_REPO = "tinyshop-me/storefront";

export const createProject = async (handle: string) => {
  const data = {
    name: handle,
    enableAffectedProjectsDeployments: true,
    environmentVariables: ENV_VARIABLES,
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

export const editEnvVariable = async (
  handle: string,
  name: string,
  value: string
) => {
  const data = {
    gitBranch: "main",
    key: name,
    target: "[production]",
    type: "encrypted",
    value: value,
  };
  await fetch(
    `https://api.vercel.com/v9/projects/${handle}/env/${name}?teamId=${VERCEL_TEAM_ID}`,
    {
      body: JSON.stringify(data),
      headers: {
        Authorization: `Bearer ${VERCEL_AUTH_TOKEN}`,
      },
      method: "patch",
    }
  );
};
