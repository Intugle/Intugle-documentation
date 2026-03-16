import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

const config: Config = {
  title: 'Intugle Documentation Portal',
  tagline: 'Vibe Coding Data products',
  favicon: 'https://intugle.ai/intugle-icon.svg',

  // Future flags, see https://docusaurus.io/docs/api/docusaurus-config#future
  future: {
    v4: true, // Improve compatibility with the upcoming Docusaurus v4
  },

  // Set the production url of your site here
  // url: 'https://intugle.github.io/',
  url: 'https://docs.intugle.ai/',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  // baseUrl: '/Intugle-documentation/',
  baseUrl: '/',

  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'intugle', // Usually your GitHub org/user name.
  projectName: 'Intugle-documentation', // Usually your repo name.

  // onBrokenLinks: 'throw',
  onBrokenLinks: 'warn',

  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      {
        docs: {
          routeBasePath: "/",
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://githu``b.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          editUrl:
            'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
          // Useful options to enforce blogging best practices
          onInlineTags: 'warn',
          onInlineAuthors: 'warn',
          onUntruncatedBlogPosts: 'warn',
        },
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themeConfig: {
    // Replace with your project's social card
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'Intugle',
      logo: {
        alt: 'Intugle Logo',
        src: 'https://intugle.ai/intugle-icon.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: 'Documentation',
        },
        // { to: '/docs/user-guide', label: 'User Guide', position: 'left' },
        {
          href: 'https://github.com/intugle',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {
              label: 'FAQ',
              to: '/docs/faqs',
            },
          ],
        },
        {
          title: 'Community',
          items: [
            {
              label: 'Slack',
              href: 'https://slack.com',
            },
            {
              label: 'Discord',
              href: 'https://discordapp.com',
            },
            // {
            //   label: 'X',
            //   href: 'https://x.com/docusaurus',
            // },
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Intugle',
              to: 'https://intugle.ai',
            },
            {
              label: 'GitHub',
              href: 'https://github.com/intugle',
            },
          ],
        },
      ],
      copyright: `Copyright © ${new Date().getFullYear()} Intugle Inc.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
