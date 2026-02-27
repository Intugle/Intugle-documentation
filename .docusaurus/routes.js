import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/Intugle-documentation/blog',
    component: ComponentCreator('/Intugle-documentation/blog', 'e49'),
    exact: true
  },
  {
    path: '/Intugle-documentation/blog/archive',
    component: ComponentCreator('/Intugle-documentation/blog/archive', 'c5b'),
    exact: true
  },
  {
    path: '/Intugle-documentation/blog/authors',
    component: ComponentCreator('/Intugle-documentation/blog/authors', 'f3f'),
    exact: true
  },
  {
    path: '/Intugle-documentation/blog/authors/all-sebastien-lorber-articles',
    component: ComponentCreator('/Intugle-documentation/blog/authors/all-sebastien-lorber-articles', '3a4'),
    exact: true
  },
  {
    path: '/Intugle-documentation/blog/authors/yangshun',
    component: ComponentCreator('/Intugle-documentation/blog/authors/yangshun', 'a68'),
    exact: true
  },
  {
    path: '/Intugle-documentation/blog/first-blog-post',
    component: ComponentCreator('/Intugle-documentation/blog/first-blog-post', '79e'),
    exact: true
  },
  {
    path: '/Intugle-documentation/blog/long-blog-post',
    component: ComponentCreator('/Intugle-documentation/blog/long-blog-post', '938'),
    exact: true
  },
  {
    path: '/Intugle-documentation/blog/mdx-blog-post',
    component: ComponentCreator('/Intugle-documentation/blog/mdx-blog-post', '126'),
    exact: true
  },
  {
    path: '/Intugle-documentation/blog/tags',
    component: ComponentCreator('/Intugle-documentation/blog/tags', '2d7'),
    exact: true
  },
  {
    path: '/Intugle-documentation/blog/tags/docusaurus',
    component: ComponentCreator('/Intugle-documentation/blog/tags/docusaurus', 'e87'),
    exact: true
  },
  {
    path: '/Intugle-documentation/blog/tags/facebook',
    component: ComponentCreator('/Intugle-documentation/blog/tags/facebook', '6f2'),
    exact: true
  },
  {
    path: '/Intugle-documentation/blog/tags/hello',
    component: ComponentCreator('/Intugle-documentation/blog/tags/hello', '541'),
    exact: true
  },
  {
    path: '/Intugle-documentation/blog/tags/hola',
    component: ComponentCreator('/Intugle-documentation/blog/tags/hola', '30a'),
    exact: true
  },
  {
    path: '/Intugle-documentation/blog/welcome',
    component: ComponentCreator('/Intugle-documentation/blog/welcome', '929'),
    exact: true
  },
  {
    path: '/Intugle-documentation/markdown-page',
    component: ComponentCreator('/Intugle-documentation/markdown-page', '09a'),
    exact: true
  },
  {
    path: '/Intugle-documentation/docs',
    component: ComponentCreator('/Intugle-documentation/docs', 'e6c'),
    routes: [
      {
        path: '/Intugle-documentation/docs',
        component: ComponentCreator('/Intugle-documentation/docs', 'e27'),
        routes: [
          {
            path: '/Intugle-documentation/docs',
            component: ComponentCreator('/Intugle-documentation/docs', 'd41'),
            routes: [
              {
                path: '/Intugle-documentation/docs/category/tutorial---basics',
                component: ComponentCreator('/Intugle-documentation/docs/category/tutorial---basics', '1e6'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Intugle-documentation/docs/category/tutorial---extras',
                component: ComponentCreator('/Intugle-documentation/docs/category/tutorial---extras', 'e56'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Intugle-documentation/docs/intro',
                component: ComponentCreator('/Intugle-documentation/docs/intro', 'f77'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Intugle-documentation/docs/tutorial-basics/congratulations',
                component: ComponentCreator('/Intugle-documentation/docs/tutorial-basics/congratulations', '19b'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Intugle-documentation/docs/tutorial-basics/create-a-blog-post',
                component: ComponentCreator('/Intugle-documentation/docs/tutorial-basics/create-a-blog-post', 'e18'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Intugle-documentation/docs/tutorial-basics/create-a-document',
                component: ComponentCreator('/Intugle-documentation/docs/tutorial-basics/create-a-document', 'e37'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Intugle-documentation/docs/tutorial-basics/create-a-page',
                component: ComponentCreator('/Intugle-documentation/docs/tutorial-basics/create-a-page', '432'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Intugle-documentation/docs/tutorial-basics/deploy-your-site',
                component: ComponentCreator('/Intugle-documentation/docs/tutorial-basics/deploy-your-site', '548'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Intugle-documentation/docs/tutorial-basics/markdown-features',
                component: ComponentCreator('/Intugle-documentation/docs/tutorial-basics/markdown-features', '4f3'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Intugle-documentation/docs/tutorial-extras/manage-docs-versions',
                component: ComponentCreator('/Intugle-documentation/docs/tutorial-extras/manage-docs-versions', '4a1'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Intugle-documentation/docs/tutorial-extras/translate-your-site',
                component: ComponentCreator('/Intugle-documentation/docs/tutorial-extras/translate-your-site', 'ce5'),
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
    path: '/Intugle-documentation/',
    component: ComponentCreator('/Intugle-documentation/', '4be'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
