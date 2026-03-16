import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/blog',
    component: ComponentCreator('/blog', 'b2f'),
    exact: true
  },
  {
    path: '/blog/archive',
    component: ComponentCreator('/blog/archive', '182'),
    exact: true
  },
  {
    path: '/blog/authors',
    component: ComponentCreator('/blog/authors', '0b7'),
    exact: true
  },
  {
    path: '/blog/authors/all-sebastien-lorber-articles',
    component: ComponentCreator('/blog/authors/all-sebastien-lorber-articles', '4a1'),
    exact: true
  },
  {
    path: '/blog/authors/yangshun',
    component: ComponentCreator('/blog/authors/yangshun', 'a68'),
    exact: true
  },
  {
    path: '/blog/first-blog-post',
    component: ComponentCreator('/blog/first-blog-post', '89a'),
    exact: true
  },
  {
    path: '/blog/long-blog-post',
    component: ComponentCreator('/blog/long-blog-post', '9ad'),
    exact: true
  },
  {
    path: '/blog/mdx-blog-post',
    component: ComponentCreator('/blog/mdx-blog-post', 'e9f'),
    exact: true
  },
  {
    path: '/blog/tags',
    component: ComponentCreator('/blog/tags', '287'),
    exact: true
  },
  {
    path: '/blog/tags/docusaurus',
    component: ComponentCreator('/blog/tags/docusaurus', '704'),
    exact: true
  },
  {
    path: '/blog/tags/facebook',
    component: ComponentCreator('/blog/tags/facebook', '858'),
    exact: true
  },
  {
    path: '/blog/tags/hello',
    component: ComponentCreator('/blog/tags/hello', '299'),
    exact: true
  },
  {
    path: '/blog/tags/hola',
    component: ComponentCreator('/blog/tags/hola', '00d'),
    exact: true
  },
  {
    path: '/blog/welcome',
    component: ComponentCreator('/blog/welcome', 'd2b'),
    exact: true
  },
  {
    path: '/markdown-page',
    component: ComponentCreator('/markdown-page', '3d7'),
    exact: true
  },
  {
    path: '/',
    component: ComponentCreator('/', 'e5f'),
    exact: true
  },
  {
    path: '/',
    component: ComponentCreator('/', '731'),
    routes: [
      {
        path: '/',
        component: ComponentCreator('/', '4ef'),
        routes: [
          {
            path: '/',
            component: ComponentCreator('/', 'a6f'),
            routes: [
              {
                path: '/Connections/adls',
                component: ComponentCreator('/Connections/adls', 'e13'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Connections/azureblob',
                component: ComponentCreator('/Connections/azureblob', '91f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Connections/bigquery',
                component: ComponentCreator('/Connections/bigquery', '044'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/databricks-engine',
                component: ComponentCreator('/databricks-engine', '793'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/databricks-engine/databricks',
                component: ComponentCreator('/databricks-engine/databricks', 'a92'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/FAQs/',
                component: ComponentCreator('/FAQs/', '562'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Intro',
                component: ComponentCreator('/Intro', '9d9'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
