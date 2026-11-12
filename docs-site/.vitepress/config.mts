import { defineConfig } from 'vitepress'

// The site is generated into src/ by src/render_site.py before VitePress builds.
// `base` must match SITE_BASE in src/render_site.py.
export default defineConfig({
  base: '/CIRS/',
  srcDir: 'src',
  title: 'CIRS',
  description: 'Community Industry Replacement Set for OpenTTD',
  head: [
    ['link', { rel: 'icon', type: 'image/png', href: '/CIRS/img/industries/integrated_steel_mill.png' }],
    ['meta', { name: 'theme-color', content: '#1f6f43' }]
  ],
  themeConfig: {
    logo: '/img/industries/integrated_steel_mill.png',
    socialLinks: [{ icon: 'github', link: 'https://github.com/Maicarons/CIRS' }],
    search: {
      provider: 'local'
    },
    outline: { level: [2, 3] }
  },
  locales: {
    root: {
      label: 'English',
      lang: 'en',
      themeConfig: {
        nav: [
          { text: 'Guide', link: '/get-started.html' },
          { text: 'Economies', link: '/economies.html' },
          { text: 'Cargos', link: '/cargos.html' },
          { text: 'Industries', link: '/industries.html' },
          {
            text: 'Reference',
            items: [
              { text: 'Code reference', link: '/code-reference.html' },
              { text: 'Changelog', link: '/changelog.html' },
              { text: 'Translations', link: '/translations.html' }
            ]
          }
        ],
        sidebar: [
          {
            text: 'Guide',
            items: [
              { text: 'Get started', link: '/get-started.html' },
              { text: 'Economies', link: '/economies.html' },
              { text: 'Cargos', link: '/cargos.html' },
              { text: 'Industries', link: '/industries.html' }
            ]
          },
          {
            text: 'Reference',
            items: [
              { text: 'Code reference', link: '/code-reference.html' },
              { text: 'Changelog', link: '/changelog.html' },
              { text: 'Translations', link: '/translations.html' }
            ]
          }
        ],
        outline: { label: 'On this page' },
        docFooter: { prev: 'Previous', next: 'Next' },
        darkModeSwitchLabel: 'Appearance',
        lightModeSwitchTitle: 'Switch to light theme',
        darkModeSwitchTitle: 'Switch to dark theme',
        sidebarMenuLabel: 'Menu',
        returnToTopLabel: 'Return to top',
        langMenuLabel: 'Change language',
        externalLinkIcon: true
      }
    },
    zh: {
      label: '简体中文',
      lang: 'zh',
      link: '/zh/',
      themeConfig: {
        nav: [
          { text: '指南', link: '/zh/get-started.html' },
          { text: '经济', link: '/zh/economies.html' },
          { text: '货物', link: '/zh/cargos.html' },
          { text: '产业', link: '/zh/industries.html' },
          {
            text: '参考',
            items: [
              { text: '代码参考', link: '/zh/code-reference.html' },
              { text: '更新日志', link: '/zh/changelog.html' },
              { text: '翻译', link: '/zh/translations.html' }
            ]
          }
        ],
        sidebar: [
          {
            text: '指南',
            items: [
              { text: '开始游戏', link: '/zh/get-started.html' },
              { text: '经济', link: '/zh/economies.html' },
              { text: '货物', link: '/zh/cargos.html' },
              { text: '产业', link: '/zh/industries.html' }
            ]
          },
          {
            text: '参考',
            items: [
              { text: '代码参考', link: '/zh/code-reference.html' },
              { text: '更新日志', link: '/zh/changelog.html' },
              { text: '翻译', link: '/zh/translations.html' }
            ]
          }
        ],
        outline: { label: '本页目录' },
        docFooter: { prev: '上一页', next: '下一页' },
        darkModeSwitchLabel: '外观',
        lightModeSwitchTitle: '切换到浅色模式',
        darkModeSwitchTitle: '切换到深色模式',
        sidebarMenuLabel: '菜单',
        returnToTopLabel: '回到顶部',
        langMenuLabel: '切换语言',
        externalLinkIcon: true
      }
    }
  }
})
