import { themes as prismThemes } from 'prism-react-renderer';
import type { Config } from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'Intugle Documentation Portal',
  tagline: 'Vibe Coding Data products',
  favicon: 'https://intugle.ai/intugle-icon.svg',

  future: {
    v4: true,
  },

  url: 'https://docs.intugle.ai/',
  baseUrl: '/',

  organizationName: 'intugle',
  projectName: 'Intugle-documentation',

  onBrokenLinks: 'warn',

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
          // editUrl:
//  'https://github.com/intugle/Intugle-documentation/tree/main/',
        },
        blog: {
          showReadingTime: true,
          feedOptions: {
            type: ['rss', 'atom'],
            xslt: true,
          },
          // editUrl:'https://github.com/intugle/Intugle-documentation/tree/main/',
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
    image: 'https://intugle.ai/intugle-icon.svg',
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
              label: 'Documentation',
              to: '/',
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
          ],
        },
        {
          title: 'More',
          items: [
            {
              label: 'Intugle',
              href: 'https://intugle.ai',
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
