const config = {
  title: "fl0w Docs",
  tagline: "Android notes, docs, and documentation",
  favicon: "assets/img/site/favicon.ico",
  url: "https://codefl0w.xyz",
  baseUrl: "/docs/",
  organizationName: "codefl0w",
  projectName: "codefl0w.github.io",
  onBrokenLinks: "warn",
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: "warn"
    }
  },
  i18n: {
    defaultLocale: "en",
    locales: ["en"]
  },
  themeConfig: {
    colorMode: {
      defaultMode: "dark",
      disableSwitch: false,
      respectPrefersColorScheme: true
    },
    navbar: {
      title: "fl0w Docs",
      items: [
        {
          to: "/",
          label: "Docs",
          position: "left"
        },
        {
          href: "https://github.com/codefl0w",
          label: "GitHub",
          position: "right"
        }
      ]
    },
    footer: {
      style: "dark",
      links: [
        {
          title: "Docs",
          items: [
            {
              label: "Intro",
              to: "/"
            }
          ]
        },
        {
          title: "More",
          items: [
            {
              label: "Archive",
              href: "https://codefl0w.xyz/archive"
            }
          ]
        }
      ],
      copyright: `Copyright ${new Date().getFullYear()} fl0w`
    }
  },
  presets: [
    [
      "classic",
      {
        docs: {
          path: "docs",
          routeBasePath: "/",
          sidebarPath: require.resolve("./sidebars.js")
        },
        blog: false,
        theme: {
          customCss: require.resolve("./src/css/custom.css")
        }
      }
    ]
  ]
};

module.exports = config;
