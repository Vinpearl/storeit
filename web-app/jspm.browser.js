SystemJS.config({
  trace: true,
  baseURL: "/",
  paths: {
    "github:*": "jspm_packages/github/*",
    "npm:*": "jspm_packages/npm/*",
    "storeIt-webapp/": "src/"
  }
});
