# Website

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

## Installation

```bash
yarn
```

## Local Development

```bash
yarn start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

## Build

```bash
yarn build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Deployment

Using SSH:

```bash
USE_SSH=true yarn deploy
```

## Post Deployment

After deployment, the DNS mapping often gets reset. Do the following:
- Go to Intugle github account
- select Intugle-Documentation repo
- Go to Settings -> Code and automation -> Pages
- 'Custom domain' should be cleared. Enter 'docs.intugle.ai' and click Save. Wait for it to effect.