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
          { text: 'CIRS Growth', link: '/cirs-growth.html' },
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
              { text: 'Industries', link: '/industries.html' },
              { text: 'CIRS Growth', link: '/cirs-growth.html' }
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
          { text: 'CIRS Growth', link: '/zh/cirs-growth.html' },
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
              { text: '产业', link: '/zh/industries.html' },
              { text: 'CIRS Growth', link: '/zh/cirs-growth.html' }
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
    },
    fr: {
      label: 'Français',
      lang: 'fr',
      link: '/fr/',
      themeConfig: {
        nav: [
          { text: 'Guide', link: '/fr/get-started.html' },
          { text: 'Économies', link: '/fr/economies.html' },
          { text: 'Marchandises', link: '/fr/cargos.html' },
          { text: 'Industries', link: '/fr/industries.html' },
          { text: 'CIRS Growth', link: '/fr/cirs-growth.html' },
          {
            text: 'Référence',
            items: [
              { text: 'Référence du code', link: '/fr/code-reference.html' },
              { text: 'Journal des modifications', link: '/fr/changelog.html' },
              { text: 'Traductions', link: '/fr/translations.html' }
            ]
          }
        ],
        sidebar: [
          {
            text: 'Guide',
            items: [
              { text: 'Démarrage', link: '/fr/get-started.html' },
              { text: 'Économies', link: '/fr/economies.html' },
              { text: 'Marchandises', link: '/fr/cargos.html' },
              { text: 'Industries', link: '/fr/industries.html' },
              { text: 'CIRS Growth', link: '/fr/cirs-growth.html' }
            ]
          },
          {
            text: 'Référence',
            items: [
              { text: 'Référence du code', link: '/fr/code-reference.html' },
              { text: 'Journal des modifications', link: '/fr/changelog.html' },
              { text: 'Traductions', link: '/fr/translations.html' }
            ]
          }
        ],
        outline: { label: 'Sur cette page' },
        docFooter: { prev: 'Précédent', next: 'Suivant' },
        darkModeSwitchLabel: 'Apparence',
        lightModeSwitchTitle: 'Passer en thème clair',
        darkModeSwitchTitle: 'Passer en thème sombre',
        sidebarMenuLabel: 'Menu',
        returnToTopLabel: 'Haut de page',
        langMenuLabel: 'Changer de langue',
        externalLinkIcon: true
      }
    },
    de: {
      label: 'Deutsch',
      lang: 'de',
      link: '/de/',
      themeConfig: {
        nav: [
          { text: 'Leitfaden', link: '/de/get-started.html' },
          { text: 'Wirtschaften', link: '/de/economies.html' },
          { text: 'Güter', link: '/de/cargos.html' },
          { text: 'Industrien', link: '/de/industries.html' },
          { text: 'CIRS Growth', link: '/de/cirs-growth.html' },
          {
            text: 'Referenz',
            items: [
              { text: 'Code-Referenz', link: '/de/code-reference.html' },
              { text: 'Änderungsprotokoll', link: '/de/changelog.html' },
              { text: 'Übersetzungen', link: '/de/translations.html' }
            ]
          }
        ],
        sidebar: [
          {
            text: 'Leitfaden',
            items: [
              { text: 'Erste Schritte', link: '/de/get-started.html' },
              { text: 'Wirtschaften', link: '/de/economies.html' },
              { text: 'Güter', link: '/de/cargos.html' },
              { text: 'Industrien', link: '/de/industries.html' },
              { text: 'CIRS Growth', link: '/de/cirs-growth.html' }
            ]
          },
          {
            text: 'Referenz',
            items: [
              { text: 'Code-Referenz', link: '/de/code-reference.html' },
              { text: 'Änderungsprotokoll', link: '/de/changelog.html' },
              { text: 'Übersetzungen', link: '/de/translations.html' }
            ]
          }
        ],
        outline: { label: 'Auf dieser Seite' },
        docFooter: { prev: 'Zurück', next: 'Weiter' },
        darkModeSwitchLabel: 'Erscheinungsbild',
        lightModeSwitchTitle: 'Zum hellen Design wechseln',
        darkModeSwitchTitle: 'Zum dunklen Design wechseln',
        sidebarMenuLabel: 'Menü',
        returnToTopLabel: 'Nach oben',
        langMenuLabel: 'Sprache ändern',
        externalLinkIcon: true
      }
    },
    es: {
      label: 'Español',
      lang: 'es',
      link: '/es/',
      themeConfig: {
        nav: [
          { text: 'Guía', link: '/es/get-started.html' },
          { text: 'Economías', link: '/es/economies.html' },
          { text: 'Mercancías', link: '/es/cargos.html' },
          { text: 'Industrias', link: '/es/industries.html' },
          { text: 'CIRS Growth', link: '/es/cirs-growth.html' },
          {
            text: 'Referencia',
            items: [
              { text: 'Referencia de código', link: '/es/code-reference.html' },
              { text: 'Registro de cambios', link: '/es/changelog.html' },
              { text: 'Traducciones', link: '/es/translations.html' }
            ]
          }
        ],
        sidebar: [
          {
            text: 'Guía',
            items: [
              { text: 'Primeros pasos', link: '/es/get-started.html' },
              { text: 'Economías', link: '/es/economies.html' },
              { text: 'Mercancías', link: '/es/cargos.html' },
              { text: 'Industrias', link: '/es/industries.html' },
              { text: 'CIRS Growth', link: '/es/cirs-growth.html' }
            ]
          },
          {
            text: 'Referencia',
            items: [
              { text: 'Referencia de código', link: '/es/code-reference.html' },
              { text: 'Registro de cambios', link: '/es/changelog.html' },
              { text: 'Traducciones', link: '/es/translations.html' }
            ]
          }
        ],
        outline: { label: 'En esta página' },
        docFooter: { prev: 'Anterior', next: 'Siguiente' },
        darkModeSwitchLabel: 'Apariencia',
        lightModeSwitchTitle: 'Cambiar a tema claro',
        darkModeSwitchTitle: 'Cambiar a tema oscuro',
        sidebarMenuLabel: 'Menú',
        returnToTopLabel: 'Volver arriba',
        langMenuLabel: 'Cambiar idioma',
        externalLinkIcon: true
      }
    },
    pt: {
      label: 'Português',
      lang: 'pt',
      link: '/pt/',
      themeConfig: {
        nav: [
          { text: 'Guia', link: '/pt/get-started.html' },
          { text: 'Economias', link: '/pt/economies.html' },
          { text: 'Cargas', link: '/pt/cargos.html' },
          { text: 'Indústrias', link: '/pt/industries.html' },
          { text: 'CIRS Growth', link: '/pt/cirs-growth.html' },
          {
            text: 'Referência',
            items: [
              { text: 'Referência de código', link: '/pt/code-reference.html' },
              { text: 'Registro de alterações', link: '/pt/changelog.html' },
              { text: 'Traduções', link: '/pt/translations.html' }
            ]
          }
        ],
        sidebar: [
          {
            text: 'Guia',
            items: [
              { text: 'Primeiros passos', link: '/pt/get-started.html' },
              { text: 'Economias', link: '/pt/economies.html' },
              { text: 'Cargas', link: '/pt/cargos.html' },
              { text: 'Indústrias', link: '/pt/industries.html' },
              { text: 'CIRS Growth', link: '/pt/cirs-growth.html' }
            ]
          },
          {
            text: 'Referência',
            items: [
              { text: 'Referência de código', link: '/pt/code-reference.html' },
              { text: 'Registro de alterações', link: '/pt/changelog.html' },
              { text: 'Traduções', link: '/pt/translations.html' }
            ]
          }
        ],
        outline: { label: 'Nesta página' },
        docFooter: { prev: 'Anterior', next: 'Próximo' },
        darkModeSwitchLabel: 'Aparência',
        lightModeSwitchTitle: 'Mudar para tema claro',
        darkModeSwitchTitle: 'Mudar para tema escuro',
        sidebarMenuLabel: 'Menu',
        returnToTopLabel: 'Voltar ao topo',
        langMenuLabel: 'Mudar idioma',
        externalLinkIcon: true
      }
    },
    ko: {
      label: '한국어',
      lang: 'ko',
      link: '/ko/',
      themeConfig: {
        nav: [
          { text: '가이드', link: '/ko/get-started.html' },
          { text: '경제', link: '/ko/economies.html' },
          { text: '화물', link: '/ko/cargos.html' },
          { text: '산업', link: '/ko/industries.html' },
          { text: 'CIRS Growth', link: '/ko/cirs-growth.html' },
          {
            text: '참조',
            items: [
              { text: '코드 참조', link: '/ko/code-reference.html' },
              { text: '변경 기록', link: '/ko/changelog.html' },
              { text: '번역', link: '/ko/translations.html' }
            ]
          }
        ],
        sidebar: [
          {
            text: '가이드',
            items: [
              { text: '시작하기', link: '/ko/get-started.html' },
              { text: '경제', link: '/ko/economies.html' },
              { text: '화물', link: '/ko/cargos.html' },
              { text: '산업', link: '/ko/industries.html' },
              { text: 'CIRS Growth', link: '/ko/cirs-growth.html' }
            ]
          },
          {
            text: '참조',
            items: [
              { text: '코드 참조', link: '/ko/code-reference.html' },
              { text: '변경 기록', link: '/ko/changelog.html' },
              { text: '번역', link: '/ko/translations.html' }
            ]
          }
        ],
        outline: { label: '이 페이지' },
        docFooter: { prev: '이전', next: '다음' },
        darkModeSwitchLabel: '모양',
        lightModeSwitchTitle: '밝은 테마로 전환',
        darkModeSwitchTitle: '어두운 테마로 전환',
        sidebarMenuLabel: '메뉴',
        returnToTopLabel: '맨 위로',
        langMenuLabel: '언어 변경',
        externalLinkIcon: true
      }
    },
    ar: {
      label: 'العربية',
      lang: 'ar',
      dir: 'rtl',
      link: '/ar/',
      themeConfig: {
        nav: [
          { text: 'دليل', link: '/ar/get-started.html' },
          { text: 'الاقتصادات', link: '/ar/economies.html' },
          { text: 'البضائع', link: '/ar/cargos.html' },
          { text: 'الصناعات', link: '/ar/industries.html' },
          { text: 'CIRS Growth', link: '/ar/cirs-growth.html' },
          {
            text: 'مرجع',
            items: [
              { text: 'مرجع الكود', link: '/ar/code-reference.html' },
              { text: 'سجل التغييرات', link: '/ar/changelog.html' },
              { text: 'الترجمات', link: '/ar/translations.html' }
            ]
          }
        ],
        sidebar: [
          {
            text: 'دليل',
            items: [
              { text: 'بدء الاستخدام', link: '/ar/get-started.html' },
              { text: 'الاقتصادات', link: '/ar/economies.html' },
              { text: 'البضائع', link: '/ar/cargos.html' },
              { text: 'الصناعات', link: '/ar/industries.html' },
              { text: 'CIRS Growth', link: '/ar/cirs-growth.html' }
            ]
          },
          {
            text: 'مرجع',
            items: [
              { text: 'مرجع الكود', link: '/ar/code-reference.html' },
              { text: 'سجل التغييرات', link: '/ar/changelog.html' },
              { text: 'الترجمات', link: '/ar/translations.html' }
            ]
          }
        ],
        outline: { label: 'في هذه الصفحة' },
        docFooter: { prev: 'السابق', next: 'التالي' },
        darkModeSwitchLabel: 'المظهر',
        lightModeSwitchTitle: 'التبديل إلى السمة الفاتحة',
        darkModeSwitchTitle: 'التبديل إلى السمة الداكنة',
        sidebarMenuLabel: 'القائمة',
        returnToTopLabel: 'العودة إلى الأعلى',
        langMenuLabel: 'تغيير اللغة',
        externalLinkIcon: true
      }
    },
    'af': {
      label: "Afrikaans",
      lang: "af",
      link: "/af/",
      themeConfig: {
        nav: [
          { text: "Gids", link: "/af/get-started.html" },
          { text: "Ekonomieë", link: "/af/economies.html" },
          { text: "Vragte", link: "/af/cargos.html" },
          { text: "Nywerhede", link: "/af/industries.html" },
          { text: "CIRS Growth", link: "/af/cirs-growth.html" },
          {
            text: "Verwysing",
            items: [
              { text: "Kodeverwysing", link: "/af/code-reference.html" },
              { text: "Veranderinge", link: "/af/changelog.html" },
              { text: "Vertalings", link: "/af/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Gids",
            items: [
              { text: "Begin nou", link: "/af/get-started.html" },
              { text: "Ekonomieë", link: "/af/economies.html" },
              { text: "Vragte", link: "/af/cargos.html" },
              { text: "Nywerhede", link: "/af/industries.html" },
              { text: "CIRS Growth", link: "/af/cirs-growth.html" }
            ]
          },
          {
            text: "Verwysing",
            items: [
              { text: "Kodeverwysing", link: "/af/code-reference.html" },
              { text: "Veranderinge", link: "/af/changelog.html" },
              { text: "Vertalings", link: "/af/translations.html" }
            ]
          }
        ],
        outline: { label: "Op hierdie bladsy" },
        docFooter: { prev: "Vorige", next: "Volgende" },
        darkModeSwitchLabel: "Uiterlik",
        lightModeSwitchTitle: "Skakel na ligte tema",
        darkModeSwitchTitle: "Skakel na donker tema",
        sidebarMenuLabel: "Kieslys",
        returnToTopLabel: "Terug bo",
        langMenuLabel: "Wissel taal",
        externalLinkIcon: true
      }
    },
    'be': {
      label: "Беларуская",
      lang: "be",
      link: "/be/",
      themeConfig: {
        nav: [
          { text: "Кіраўніцтва", link: "/be/get-started.html" },
          { text: "Гаспадаркі", link: "/be/economies.html" },
          { text: "Грузы", link: "/be/cargos.html" },
          { text: "Галіны прамысловасці", link: "/be/industries.html" },
          { text: "CIRS Growth", link: "/be/cirs-growth.html" },
          {
            text: "Спасылкі",
            items: [
              { text: "Даведнік па кодзе", link: "/be/code-reference.html" },
              { text: "Спіс змен", link: "/be/changelog.html" },
              { text: "Пераклады", link: "/be/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Кіраўніцтва",
            items: [
              { text: "Пачаць", link: "/be/get-started.html" },
              { text: "Гаспадаркі", link: "/be/economies.html" },
              { text: "Грузы", link: "/be/cargos.html" },
              { text: "Галіны прамысловасці", link: "/be/industries.html" },
              { text: "CIRS Growth", link: "/be/cirs-growth.html" }
            ]
          },
          {
            text: "Спасылкі",
            items: [
              { text: "Даведнік па кодзе", link: "/be/code-reference.html" },
              { text: "Спіс змен", link: "/be/changelog.html" },
              { text: "Пераклады", link: "/be/translations.html" }
            ]
          }
        ],
        outline: { label: "На гэтай старонцы" },
        docFooter: { prev: "Папярэдні", next: "Наступны" },
        darkModeSwitchLabel: "Від",
        lightModeSwitchTitle: "Пераключыць на светлую тэму",
        darkModeSwitchTitle: "Пераключыць на цёмную тэму",
        sidebarMenuLabel: "Меню",
        returnToTopLabel: "Вярнуцца наверх",
        langMenuLabel: "Змяніць мову",
        externalLinkIcon: true
      }
    },
    'ca': {
      label: "Català",
      lang: "ca",
      link: "/ca/",
      themeConfig: {
        nav: [
          { text: "Guia", link: "/ca/get-started.html" },
          { text: "Economies", link: "/ca/economies.html" },
          { text: "Càrregues", link: "/ca/cargos.html" },
          { text: "Indústries", link: "/ca/industries.html" },
          { text: "CIRS Growth", link: "/ca/cirs-growth.html" },
          {
            text: "Referència",
            items: [
              { text: "Referència de codi", link: "/ca/code-reference.html" },
              { text: "Registre de canvis", link: "/ca/changelog.html" },
              { text: "Traduccions", link: "/ca/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Guia",
            items: [
              { text: "Començar", link: "/ca/get-started.html" },
              { text: "Economies", link: "/ca/economies.html" },
              { text: "Càrregues", link: "/ca/cargos.html" },
              { text: "Indústries", link: "/ca/industries.html" },
              { text: "CIRS Growth", link: "/ca/cirs-growth.html" }
            ]
          },
          {
            text: "Referència",
            items: [
              { text: "Referència de codi", link: "/ca/code-reference.html" },
              { text: "Registre de canvis", link: "/ca/changelog.html" },
              { text: "Traduccions", link: "/ca/translations.html" }
            ]
          }
        ],
        outline: { label: "En aquesta pàgina" },
        docFooter: { prev: "Anterior", next: "Següent" },
        darkModeSwitchLabel: "Aparència",
        lightModeSwitchTitle: "Canvia al tema clar",
        darkModeSwitchTitle: "Canvia al tema fosc",
        sidebarMenuLabel: "Menú",
        returnToTopLabel: "Torna dalt",
        langMenuLabel: "Canvia d'idioma",
        externalLinkIcon: true
      }
    },
    'cs': {
      label: "Čeština",
      lang: "cs",
      link: "/cs/",
      themeConfig: {
        nav: [
          { text: "Průvodce", link: "/cs/get-started.html" },
          { text: "Ekonomiky", link: "/cs/economies.html" },
          { text: "Náklady", link: "/cs/cargos.html" },
          { text: "Průmyslová odvětví", link: "/cs/industries.html" },
          { text: "CIRS Growth", link: "/cs/cirs-growth.html" },
          {
            text: "Reference",
            items: [
              { text: "Reference kódu", link: "/cs/code-reference.html" },
              { text: "Seznam změn", link: "/cs/changelog.html" },
              { text: "Překlady", link: "/cs/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Průvodce",
            items: [
              { text: "Začít", link: "/cs/get-started.html" },
              { text: "Ekonomiky", link: "/cs/economies.html" },
              { text: "Náklady", link: "/cs/cargos.html" },
              { text: "Průmyslová odvětví", link: "/cs/industries.html" },
              { text: "CIRS Growth", link: "/cs/cirs-growth.html" }
            ]
          },
          {
            text: "Reference",
            items: [
              { text: "Reference kódu", link: "/cs/code-reference.html" },
              { text: "Seznam změn", link: "/cs/changelog.html" },
              { text: "Překlady", link: "/cs/translations.html" }
            ]
          }
        ],
        outline: { label: "Na této stránce" },
        docFooter: { prev: "Předchozí", next: "Další" },
        darkModeSwitchLabel: "Vzhled",
        lightModeSwitchTitle: "Přepnout na světlé téma",
        darkModeSwitchTitle: "Přepnout na tmavé téma",
        sidebarMenuLabel: "Menu",
        returnToTopLabel: "Návrat nahoru",
        langMenuLabel: "Změnit jazyk",
        externalLinkIcon: true
      }
    },
    'cy': {
      label: "Cymraeg",
      lang: "cy",
      link: "/cy/",
      themeConfig: {
        nav: [
          { text: "Canllaw", link: "/cy/get-started.html" },
          { text: "Economïau", link: "/cy/economies.html" },
          { text: "Cludiant", link: "/cy/cargos.html" },
          { text: "Diwydiannau", link: "/cy/industries.html" },
          { text: "CIRS Growth", link: "/cy/cirs-growth.html" },
          {
            text: "Cyfeiriad",
            items: [
              { text: "Cyfeirnod Côd", link: "/cy/code-reference.html" },
              { text: "Cofnod Newidiadau", link: "/cy/changelog.html" },
              { text: "Cyfieithiadau", link: "/cy/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Canllaw",
            items: [
              { text: "Dechrau", link: "/cy/get-started.html" },
              { text: "Economïau", link: "/cy/economies.html" },
              { text: "Cludiant", link: "/cy/cargos.html" },
              { text: "Diwydiannau", link: "/cy/industries.html" },
              { text: "CIRS Growth", link: "/cy/cirs-growth.html" }
            ]
          },
          {
            text: "Cyfeiriad",
            items: [
              { text: "Cyfeirnod Côd", link: "/cy/code-reference.html" },
              { text: "Cofnod Newidiadau", link: "/cy/changelog.html" },
              { text: "Cyfieithiadau", link: "/cy/translations.html" }
            ]
          }
        ],
        outline: { label: "Ar y dudalen hon" },
        docFooter: { prev: "Cynt", next: "Nes" },
        darkModeSwitchLabel: "Ymddangosiad",
        lightModeSwitchTitle: "Newid i thema golau",
        darkModeSwitchTitle: "Newid i thema tywyll",
        sidebarMenuLabel: "Prifddewis",
        returnToTopLabel: "Dychwelyd i'r brig",
        langMenuLabel: "Newid iaith",
        externalLinkIcon: true
      }
    },
    'da': {
      label: "Dansk",
      lang: "da",
      link: "/da/",
      themeConfig: {
        nav: [
          { text: "Guide", link: "/da/get-started.html" },
          { text: "Økonomier", link: "/da/economies.html" },
          { text: "Godsvarer", link: "/da/cargos.html" },
          { text: "Industrier", link: "/da/industries.html" },
          { text: "CIRS Growth", link: "/da/cirs-growth.html" },
          {
            text: "Reference",
            items: [
              { text: "Kodereference", link: "/da/code-reference.html" },
              { text: "Ændringslog", link: "/da/changelog.html" },
              { text: "Oversættelser", link: "/da/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Guide",
            items: [
              { text: "Kom i gang", link: "/da/get-started.html" },
              { text: "Økonomier", link: "/da/economies.html" },
              { text: "Godsvarer", link: "/da/cargos.html" },
              { text: "Industrier", link: "/da/industries.html" },
              { text: "CIRS Growth", link: "/da/cirs-growth.html" }
            ]
          },
          {
            text: "Reference",
            items: [
              { text: "Kodereference", link: "/da/code-reference.html" },
              { text: "Ændringslog", link: "/da/changelog.html" },
              { text: "Oversættelser", link: "/da/translations.html" }
            ]
          }
        ],
        outline: { label: "På denne side" },
        docFooter: { prev: "Forrige", next: "Næste" },
        darkModeSwitchLabel: "Udseende",
        lightModeSwitchTitle: "Skift til lys tema",
        darkModeSwitchTitle: "Skift til mørkt tema",
        sidebarMenuLabel: "Menu",
        returnToTopLabel: "Tilbage til toppen",
        langMenuLabel: "Skift sprog",
        externalLinkIcon: true
      }
    },
    'eo': {
      label: "Esperanto",
      lang: "eo",
      link: "/eo/",
      themeConfig: {
        nav: [
          { text: "Gvidilo", link: "/eo/get-started.html" },
          { text: "Ekonomioj", link: "/eo/economies.html" },
          { text: "Varoj", link: "/eo/cargos.html" },
          { text: "Industrioj", link: "/eo/industries.html" },
          { text: "CIRS Growth", link: "/eo/cirs-growth.html" },
          {
            text: "Referenco",
            items: [
              { text: "Koda Referenco", link: "/eo/code-reference.html" },
              { text: "Ŝanĝoprotokolo", link: "/eo/changelog.html" },
              { text: "Tradukoj", link: "/eo/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Gvidilo",
            items: [
              { text: "Ekomi", link: "/eo/get-started.html" },
              { text: "Ekonomioj", link: "/eo/economies.html" },
              { text: "Varoj", link: "/eo/cargos.html" },
              { text: "Industrioj", link: "/eo/industries.html" },
              { text: "CIRS Growth", link: "/eo/cirs-growth.html" }
            ]
          },
          {
            text: "Referenco",
            items: [
              { text: "Koda Referenco", link: "/eo/code-reference.html" },
              { text: "Ŝanĝoprotokolo", link: "/eo/changelog.html" },
              { text: "Tradukoj", link: "/eo/translations.html" }
            ]
          }
        ],
        outline: { label: "Sur ĉi tiu paĝo" },
        docFooter: { prev: "Antaŭa", next: "Sekva" },
        darkModeSwitchLabel: "Aspekto",
        lightModeSwitchTitle: "Ŝanĝu al hela temo",
        darkModeSwitchTitle: "Ŝanĝu al malhela temo",
        sidebarMenuLabel: "Menuo",
        returnToTopLabel: "Reiru al la supra parto",
        langMenuLabel: "Ŝanĝu la lingvon",
        externalLinkIcon: true
      }
    },
    'es-mx': {
      label: "Español (MX)",
      lang: "es-mx",
      link: "/es-mx/",
      themeConfig: {
        nav: [
          { text: "Guía", link: "/es-mx/get-started.html" },
          { text: "Economías", link: "/es-mx/economies.html" },
          { text: "Cargas", link: "/es-mx/cargos.html" },
          { text: "Industrias", link: "/es-mx/industries.html" },
          { text: "CIRS Growth", link: "/es-mx/cirs-growth.html" },
          {
            text: "Referencia",
            items: [
              { text: "Referencia de código", link: "/es-mx/code-reference.html" },
              { text: "Registro de cambios", link: "/es-mx/changelog.html" },
              { text: "Traducciones", link: "/es-mx/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Guía",
            items: [
              { text: "Empezar", link: "/es-mx/get-started.html" },
              { text: "Economías", link: "/es-mx/economies.html" },
              { text: "Cargas", link: "/es-mx/cargos.html" },
              { text: "Industrias", link: "/es-mx/industries.html" },
              { text: "CIRS Growth", link: "/es-mx/cirs-growth.html" }
            ]
          },
          {
            text: "Referencia",
            items: [
              { text: "Referencia de código", link: "/es-mx/code-reference.html" },
              { text: "Registro de cambios", link: "/es-mx/changelog.html" },
              { text: "Traducciones", link: "/es-mx/translations.html" }
            ]
          }
        ],
        outline: { label: "En esta página" },
        docFooter: { prev: "Anterior", next: "Siguiente" },
        darkModeSwitchLabel: "Apariencia",
        lightModeSwitchTitle: "Cambiar a tema claro",
        darkModeSwitchTitle: "Cambiar a tema oscuro",
        sidebarMenuLabel: "Menú",
        returnToTopLabel: "Volver arriba",
        langMenuLabel: "Cambiar idioma",
        externalLinkIcon: true
      }
    },
    'et': {
      label: "Eesti",
      lang: "et",
      link: "/et/",
      themeConfig: {
        nav: [
          { text: "Juhend", link: "/et/get-started.html" },
          { text: "Majandused", link: "/et/economies.html" },
          { text: "Veosed", link: "/et/cargos.html" },
          { text: "Tööstused", link: "/et/industries.html" },
          { text: "CIRS Growth", link: "/et/cirs-growth.html" },
          {
            text: "Viide",
            items: [
              { text: "Koodi viide", link: "/et/code-reference.html" },
              { text: "Muudatuste logi", link: "/et/changelog.html" },
              { text: "Tõlked", link: "/et/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Juhend",
            items: [
              { text: "Alustamine", link: "/et/get-started.html" },
              { text: "Majandused", link: "/et/economies.html" },
              { text: "Veosed", link: "/et/cargos.html" },
              { text: "Tööstused", link: "/et/industries.html" },
              { text: "CIRS Growth", link: "/et/cirs-growth.html" }
            ]
          },
          {
            text: "Viide",
            items: [
              { text: "Koodi viide", link: "/et/code-reference.html" },
              { text: "Muudatuste logi", link: "/et/changelog.html" },
              { text: "Tõlked", link: "/et/translations.html" }
            ]
          }
        ],
        outline: { label: "Sellel lehel" },
        docFooter: { prev: "Eelmine", next: "Järgmine" },
        darkModeSwitchLabel: "Välimus",
        lightModeSwitchTitle: "Lülita heledale teemale",
        darkModeSwitchTitle: "Lülita tumedale teemale",
        sidebarMenuLabel: "Menüü",
        returnToTopLabel: "Tagasi üles",
        langMenuLabel: "Muuda keelt",
        externalLinkIcon: true
      }
    },
    'fi': {
      label: "Suomi",
      lang: "fi",
      link: "/fi/",
      themeConfig: {
        nav: [
          { text: "Opas", link: "/fi/get-started.html" },
          { text: "Talousjärjestelmät", link: "/fi/economies.html" },
          { text: "Rahtitavarat", link: "/fi/cargos.html" },
          { text: "Teollisuus", link: "/fi/industries.html" },
          { text: "CIRS Growth", link: "/fi/cirs-growth.html" },
          {
            text: "Viitteet",
            items: [
              { text: "Koodiviite", link: "/fi/code-reference.html" },
              { text: "Muutosloki", link: "/fi/changelog.html" },
              { text: "Käännökset", link: "/fi/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Opas",
            items: [
              { text: "Aloita", link: "/fi/get-started.html" },
              { text: "Talousjärjestelmät", link: "/fi/economies.html" },
              { text: "Rahtitavarat", link: "/fi/cargos.html" },
              { text: "Teollisuus", link: "/fi/industries.html" },
              { text: "CIRS Growth", link: "/fi/cirs-growth.html" }
            ]
          },
          {
            text: "Viitteet",
            items: [
              { text: "Koodiviite", link: "/fi/code-reference.html" },
              { text: "Muutosloki", link: "/fi/changelog.html" },
              { text: "Käännökset", link: "/fi/translations.html" }
            ]
          }
        ],
        outline: { label: "Tällä sivulla" },
        docFooter: { prev: "Edellinen", next: "Seuraava" },
        darkModeSwitchLabel: "Ulkoasu",
        lightModeSwitchTitle: "Vaihda vaaleaan teemaan",
        darkModeSwitchTitle: "Vaihda tummaan teemaan",
        sidebarMenuLabel: "Valikko",
        returnToTopLabel: "Palaa ylös",
        langMenuLabel: "Vaihda kieli",
        externalLinkIcon: true
      }
    },
    'gd': {
      label: "Gàidhlig",
      lang: "gd",
      link: "/gd/",
      themeConfig: {
        nav: [
          { text: "Stiùireadh", link: "/gd/get-started.html" },
          { text: "Eaconamaidhean", link: "/gd/economies.html" },
          { text: "Bathar", link: "/gd/cargos.html" },
          { text: "Gnìomhachasan", link: "/gd/industries.html" },
          { text: "CIRS Growth", link: "/gd/cirs-growth.html" },
          {
            text: "Iomradh",
            items: [
              { text: "Reifreans Còd", link: "/gd/code-reference.html" },
              { text: "Clàr nan Atharraichean", link: "/gd/changelog.html" },
              { text: "Eadar-theangachaidhean", link: "/gd/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Stiùireadh",
            items: [
              { text: "Tòisich", link: "/gd/get-started.html" },
              { text: "Eaconamaidhean", link: "/gd/economies.html" },
              { text: "Bathar", link: "/gd/cargos.html" },
              { text: "Gnìomhachasan", link: "/gd/industries.html" },
              { text: "CIRS Growth", link: "/gd/cirs-growth.html" }
            ]
          },
          {
            text: "Iomradh",
            items: [
              { text: "Reifreans Còd", link: "/gd/code-reference.html" },
              { text: "Clàr nan Atharraichean", link: "/gd/changelog.html" },
              { text: "Eadar-theangachaidhean", link: "/gd/translations.html" }
            ]
          }
        ],
        outline: { label: "Air an duilleag seo" },
        docFooter: { prev: "Roimhe", next: "An ath rud" },
        darkModeSwitchLabel: "Coltas",
        lightModeSwitchTitle: "Atharraich gu teama soilleir",
        darkModeSwitchTitle: "Atharraich gu teama dorcha",
        sidebarMenuLabel: "Biadh",
        returnToTopLabel: "Till chun a’ mhullach",
        langMenuLabel: "Atharraich cànan",
        externalLinkIcon: true
      }
    },
    'gl': {
      label: "Galego",
      lang: "gl",
      link: "/gl/",
      themeConfig: {
        nav: [
          { text: "Guía", link: "/gl/get-started.html" },
          { text: "Economías", link: "/gl/economies.html" },
          { text: "Cargas", link: "/gl/cargos.html" },
          { text: "Industrias", link: "/gl/industries.html" },
          { text: "CIRS Growth", link: "/gl/cirs-growth.html" },
          {
            text: "Referencia",
            items: [
              { text: "Referencia de código", link: "/gl/code-reference.html" },
              { text: "Rexistro de cambios", link: "/gl/changelog.html" },
              { text: "Traducións", link: "/gl/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Guía",
            items: [
              { text: "Comezar", link: "/gl/get-started.html" },
              { text: "Economías", link: "/gl/economies.html" },
              { text: "Cargas", link: "/gl/cargos.html" },
              { text: "Industrias", link: "/gl/industries.html" },
              { text: "CIRS Growth", link: "/gl/cirs-growth.html" }
            ]
          },
          {
            text: "Referencia",
            items: [
              { text: "Referencia de código", link: "/gl/code-reference.html" },
              { text: "Rexistro de cambios", link: "/gl/changelog.html" },
              { text: "Traducións", link: "/gl/translations.html" }
            ]
          }
        ],
        outline: { label: "Nesta páxina" },
        docFooter: { prev: "Anterior", next: "Seguinte" },
        darkModeSwitchLabel: "Apariencia",
        lightModeSwitchTitle: "Cambiar ao tema claro",
        darkModeSwitchTitle: "Cambiar ao tema escuro",
        sidebarMenuLabel: "Menú",
        returnToTopLabel: "Volver ao inicio",
        langMenuLabel: "Cambiar idioma",
        externalLinkIcon: true
      }
    },
    'hr': {
      label: "Hrvatski",
      lang: "hr",
      link: "/hr/",
      themeConfig: {
        nav: [
          { text: "Vodič", link: "/hr/get-started.html" },
          { text: "Ekonomije", link: "/hr/economies.html" },
          { text: "Tereti", link: "/hr/cargos.html" },
          { text: "Industrije", link: "/hr/industries.html" },
          { text: "CIRS Growth", link: "/hr/cirs-growth.html" },
          {
            text: "Referenca",
            items: [
              { text: "Referenca koda", link: "/hr/code-reference.html" },
              { text: "Popis promjena", link: "/hr/changelog.html" },
              { text: "Prijevodi", link: "/hr/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Vodič",
            items: [
              { text: "Započnite", link: "/hr/get-started.html" },
              { text: "Ekonomije", link: "/hr/economies.html" },
              { text: "Tereti", link: "/hr/cargos.html" },
              { text: "Industrije", link: "/hr/industries.html" },
              { text: "CIRS Growth", link: "/hr/cirs-growth.html" }
            ]
          },
          {
            text: "Referenca",
            items: [
              { text: "Referenca koda", link: "/hr/code-reference.html" },
              { text: "Popis promjena", link: "/hr/changelog.html" },
              { text: "Prijevodi", link: "/hr/translations.html" }
            ]
          }
        ],
        outline: { label: "Na ovoj stranici" },
        docFooter: { prev: "Prethodno", next: "Sljedeće" },
        darkModeSwitchLabel: "Izgled",
        lightModeSwitchTitle: "Prebacite na svijetlu temu",
        darkModeSwitchTitle: "Prebacite na tamnu temu",
        sidebarMenuLabel: "Izbornik",
        returnToTopLabel: "Vratite se na vrh",
        langMenuLabel: "Promijenite jezik",
        externalLinkIcon: true
      }
    },
    'hu': {
      label: "Magyar",
      lang: "hu",
      link: "/hu/",
      themeConfig: {
        nav: [
          { text: "Útmutató", link: "/hu/get-started.html" },
          { text: "Gazdaságok", link: "/hu/economies.html" },
          { text: "Rakományok", link: "/hu/cargos.html" },
          { text: "Iparágak", link: "/hu/industries.html" },
          { text: "CIRS Growth", link: "/hu/cirs-growth.html" },
          {
            text: "Referencia",
            items: [
              { text: "Kódreferencia", link: "/hu/code-reference.html" },
              { text: "Változásnapló", link: "/hu/changelog.html" },
              { text: "Fordítások", link: "/hu/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Útmutató",
            items: [
              { text: "Kezdés", link: "/hu/get-started.html" },
              { text: "Gazdaságok", link: "/hu/economies.html" },
              { text: "Rakományok", link: "/hu/cargos.html" },
              { text: "Iparágak", link: "/hu/industries.html" },
              { text: "CIRS Growth", link: "/hu/cirs-growth.html" }
            ]
          },
          {
            text: "Referencia",
            items: [
              { text: "Kódreferencia", link: "/hu/code-reference.html" },
              { text: "Változásnapló", link: "/hu/changelog.html" },
              { text: "Fordítások", link: "/hu/translations.html" }
            ]
          }
        ],
        outline: { label: "Ezen az oldalon" },
        docFooter: { prev: "Előző", next: "Következő" },
        darkModeSwitchLabel: "Kinézet",
        lightModeSwitchTitle: "Váltás világos témára",
        darkModeSwitchTitle: "Váltás sötét témára",
        sidebarMenuLabel: "Menü",
        returnToTopLabel: "Vissza a lap tetejére",
        langMenuLabel: "Nyelv váltása",
        externalLinkIcon: true
      }
    },
    'id': {
      label: "Indonesia",
      lang: "id",
      link: "/id/",
      themeConfig: {
        nav: [
          { text: "Panduan", link: "/id/get-started.html" },
          { text: "Ekonomi", link: "/id/economies.html" },
          { text: "Muatan", link: "/id/cargos.html" },
          { text: "Industri", link: "/id/industries.html" },
          { text: "CIRS Growth", link: "/id/cirs-growth.html" },
          {
            text: "Referensi",
            items: [
              { text: "Referensi Kode", link: "/id/code-reference.html" },
              { text: "Catatan Perubahan", link: "/id/changelog.html" },
              { text: "Terjemahan", link: "/id/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Panduan",
            items: [
              { text: "Mulai", link: "/id/get-started.html" },
              { text: "Ekonomi", link: "/id/economies.html" },
              { text: "Muatan", link: "/id/cargos.html" },
              { text: "Industri", link: "/id/industries.html" },
              { text: "CIRS Growth", link: "/id/cirs-growth.html" }
            ]
          },
          {
            text: "Referensi",
            items: [
              { text: "Referensi Kode", link: "/id/code-reference.html" },
              { text: "Catatan Perubahan", link: "/id/changelog.html" },
              { text: "Terjemahan", link: "/id/translations.html" }
            ]
          }
        ],
        outline: { label: "Di halaman ini" },
        docFooter: { prev: "Sebelumnya", next: "Berikutnya" },
        darkModeSwitchLabel: "Tampilan",
        lightModeSwitchTitle: "Beralih ke tema terang",
        darkModeSwitchTitle: "Beralih ke tema gelap",
        sidebarMenuLabel: "Menu",
        returnToTopLabel: "Kembali ke atas",
        langMenuLabel: "Ganti bahasa",
        externalLinkIcon: true
      }
    },
    'it': {
      label: "Italiano",
      lang: "it",
      link: "/it/",
      themeConfig: {
        nav: [
          { text: "Guide", link: "/it/get-started.html" },
          { text: "Economie", link: "/it/economies.html" },
          { text: "Carichi", link: "/it/cargos.html" },
          { text: "Industrie", link: "/it/industries.html" },
          { text: "CIRS Growth", link: "/it/cirs-growth.html" },
          {
            text: "Riferimenti",
            items: [
              { text: "Riferimento al codice", link: "/it/code-reference.html" },
              { text: "Registro delle modifiche", link: "/it/changelog.html" },
              { text: "Traduzioni", link: "/it/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Guide",
            items: [
              { text: "Inizia", link: "/it/get-started.html" },
              { text: "Economie", link: "/it/economies.html" },
              { text: "Carichi", link: "/it/cargos.html" },
              { text: "Industrie", link: "/it/industries.html" },
              { text: "CIRS Growth", link: "/it/cirs-growth.html" }
            ]
          },
          {
            text: "Riferimenti",
            items: [
              { text: "Riferimento al codice", link: "/it/code-reference.html" },
              { text: "Registro delle modifiche", link: "/it/changelog.html" },
              { text: "Traduzioni", link: "/it/translations.html" }
            ]
          }
        ],
        outline: { label: "In questa pagina" },
        docFooter: { prev: "Precedente", next: "Successivo" },
        darkModeSwitchLabel: "Aspetto",
        lightModeSwitchTitle: "Passa al tema chiaro",
        darkModeSwitchTitle: "Passa al tema scuro",
        sidebarMenuLabel: "Menu",
        returnToTopLabel: "Torna in alto",
        langMenuLabel: "Cambia lingua",
        externalLinkIcon: true
      }
    },
    'ja': {
      label: "日本語",
      lang: "ja",
      link: "/ja/",
      themeConfig: {
        nav: [
          { text: "ガイド", link: "/ja/get-started.html" },
          { text: "経済", link: "/ja/economies.html" },
          { text: "積荷", link: "/ja/cargos.html" },
          { text: "産業", link: "/ja/industries.html" },
          { text: "CIRS Growth", link: "/ja/cirs-growth.html" },
          {
            text: "リファレンス",
            items: [
              { text: "コードリファレンス", link: "/ja/code-reference.html" },
              { text: "変更履歴", link: "/ja/changelog.html" },
              { text: "翻訳", link: "/ja/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "ガイド",
            items: [
              { text: "始める", link: "/ja/get-started.html" },
              { text: "経済", link: "/ja/economies.html" },
              { text: "積荷", link: "/ja/cargos.html" },
              { text: "産業", link: "/ja/industries.html" },
              { text: "CIRS Growth", link: "/ja/cirs-growth.html" }
            ]
          },
          {
            text: "リファレンス",
            items: [
              { text: "コードリファレンス", link: "/ja/code-reference.html" },
              { text: "変更履歴", link: "/ja/changelog.html" },
              { text: "翻訳", link: "/ja/translations.html" }
            ]
          }
        ],
        outline: { label: "このページ" },
        docFooter: { prev: "前へ", next: "次へ" },
        darkModeSwitchLabel: "外観",
        lightModeSwitchTitle: "ライトテーマに切り替える",
        darkModeSwitchTitle: "ダークテーマに切り替える",
        sidebarMenuLabel: "メニュー",
        returnToTopLabel: "トップに戻る",
        langMenuLabel: "言語を変更",
        externalLinkIcon: true
      }
    },
    'la': {
      label: "Latina",
      lang: "la",
      link: "/la/",
      themeConfig: {
        nav: [
          { text: "Manuale", link: "/la/get-started.html" },
          { text: "Oeconomiae", link: "/la/economies.html" },
          { text: "Onera", link: "/la/cargos.html" },
          { text: "Industriae", link: "/la/industries.html" },
          { text: "CIRS Growth", link: "/la/cirs-growth.html" },
          {
            text: "Referentia",
            items: [
              { text: "Index Codicis", link: "/la/code-reference.html" },
              { text: "Acta Mutationum", link: "/la/changelog.html" },
              { text: "Translationes", link: "/la/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Manuale",
            items: [
              { text: "Incipiamus", link: "/la/get-started.html" },
              { text: "Oeconomiae", link: "/la/economies.html" },
              { text: "Onera", link: "/la/cargos.html" },
              { text: "Industriae", link: "/la/industries.html" },
              { text: "CIRS Growth", link: "/la/cirs-growth.html" }
            ]
          },
          {
            text: "Referentia",
            items: [
              { text: "Index Codicis", link: "/la/code-reference.html" },
              { text: "Acta Mutationum", link: "/la/changelog.html" },
              { text: "Translationes", link: "/la/translations.html" }
            ]
          }
        ],
        outline: { label: "In hac pagina" },
        docFooter: { prev: "Praecedens", next: "Sequens" },
        darkModeSwitchLabel: "Species",
        lightModeSwitchTitle: "Ad thema lucidum transi",
        darkModeSwitchTitle: "Ad thema obscurum transi",
        sidebarMenuLabel: "Menus",
        returnToTopLabel: "Ad summum redi",
        langMenuLabel: "Lingua mutetur",
        externalLinkIcon: true
      }
    },
    'lb': {
      label: "Lëtzebuergesch",
      lang: "lb",
      link: "/lb/",
      themeConfig: {
        nav: [
          { text: "Guide", link: "/lb/get-started.html" },
          { text: "Ekonomien", link: "/lb/economies.html" },
          { text: "Gidder", link: "/lb/cargos.html" },
          { text: "Industrien", link: "/lb/industries.html" },
          { text: "CIRS Growth", link: "/lb/cirs-growth.html" },
          {
            text: "Referenz",
            items: [
              { text: "Code-Referenz", link: "/lb/code-reference.html" },
              { text: "Ännerungsprotokoll", link: "/lb/changelog.html" },
              { text: "Iwwersetzungen", link: "/lb/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Guide",
            items: [
              { text: "Ufänken", link: "/lb/get-started.html" },
              { text: "Ekonomien", link: "/lb/economies.html" },
              { text: "Gidder", link: "/lb/cargos.html" },
              { text: "Industrien", link: "/lb/industries.html" },
              { text: "CIRS Growth", link: "/lb/cirs-growth.html" }
            ]
          },
          {
            text: "Referenz",
            items: [
              { text: "Code-Referenz", link: "/lb/code-reference.html" },
              { text: "Ännerungsprotokoll", link: "/lb/changelog.html" },
              { text: "Iwwersetzungen", link: "/lb/translations.html" }
            ]
          }
        ],
        outline: { label: "Op dëser Säit" },
        docFooter: { prev: "Viregt", next: "Nächst" },
        darkModeSwitchLabel: "Ausgesinn",
        lightModeSwitchTitle: "Op liicht Theme wiesselen",
        darkModeSwitchTitle: "Op däischtert Theme wiesselen",
        sidebarMenuLabel: "Menü",
        returnToTopLabel: "Zréck no uewen",
        langMenuLabel: "Sprooch wiesselen",
        externalLinkIcon: true
      }
    },
    'nb': {
      label: "Norsk (Bokmål)",
      lang: "nb",
      link: "/nb/",
      themeConfig: {
        nav: [
          { text: "Veiledning", link: "/nb/get-started.html" },
          { text: "Økonomier", link: "/nb/economies.html" },
          { text: "Varer", link: "/nb/cargos.html" },
          { text: "Industrier", link: "/nb/industries.html" },
          { text: "CIRS Growth", link: "/nb/cirs-growth.html" },
          {
            text: "Referanse",
            items: [
              { text: "Kodereferanse", link: "/nb/code-reference.html" },
              { text: "Endringslogg", link: "/nb/changelog.html" },
              { text: "Oversettelser", link: "/nb/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Veiledning",
            items: [
              { text: "Kom i gang", link: "/nb/get-started.html" },
              { text: "Økonomier", link: "/nb/economies.html" },
              { text: "Varer", link: "/nb/cargos.html" },
              { text: "Industrier", link: "/nb/industries.html" },
              { text: "CIRS Growth", link: "/nb/cirs-growth.html" }
            ]
          },
          {
            text: "Referanse",
            items: [
              { text: "Kodereferanse", link: "/nb/code-reference.html" },
              { text: "Endringslogg", link: "/nb/changelog.html" },
              { text: "Oversettelser", link: "/nb/translations.html" }
            ]
          }
        ],
        outline: { label: "På denne siden" },
        docFooter: { prev: "Forrige", next: "Neste" },
        darkModeSwitchLabel: "Utseende",
        lightModeSwitchTitle: "Bytt til lys tema",
        darkModeSwitchTitle: "Bytt til mørkt tema",
        sidebarMenuLabel: "Meny",
        returnToTopLabel: "Tilbake til toppen",
        langMenuLabel: "Endre språk",
        externalLinkIcon: true
      }
    },
    'nl': {
      label: "Nederlands",
      lang: "nl",
      link: "/nl/",
      themeConfig: {
        nav: [
          { text: "Gids", link: "/nl/get-started.html" },
          { text: "Economieën", link: "/nl/economies.html" },
          { text: "Goederen", link: "/nl/cargos.html" },
          { text: "Industrieën", link: "/nl/industries.html" },
          { text: "CIRS Growth", link: "/nl/cirs-growth.html" },
          {
            text: "Referentie",
            items: [
              { text: "Codereferentie", link: "/nl/code-reference.html" },
              { text: "Wijzigingslog", link: "/nl/changelog.html" },
              { text: "Vertalingen", link: "/nl/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Gids",
            items: [
              { text: "Aan de slag", link: "/nl/get-started.html" },
              { text: "Economieën", link: "/nl/economies.html" },
              { text: "Goederen", link: "/nl/cargos.html" },
              { text: "Industrieën", link: "/nl/industries.html" },
              { text: "CIRS Growth", link: "/nl/cirs-growth.html" }
            ]
          },
          {
            text: "Referentie",
            items: [
              { text: "Codereferentie", link: "/nl/code-reference.html" },
              { text: "Wijzigingslog", link: "/nl/changelog.html" },
              { text: "Vertalingen", link: "/nl/translations.html" }
            ]
          }
        ],
        outline: { label: "Op deze pagina" },
        docFooter: { prev: "Vorige", next: "Volgende" },
        darkModeSwitchLabel: "Uiterlijk",
        lightModeSwitchTitle: "Schakel over naar lichte thema",
        darkModeSwitchTitle: "Schakel over naar donkere thema",
        sidebarMenuLabel: "Menu",
        returnToTopLabel: "Terug naar boven",
        langMenuLabel: "Taal wijzigen",
        externalLinkIcon: true
      }
    },
    'pl': {
      label: "Polski",
      lang: "pl",
      link: "/pl/",
      themeConfig: {
        nav: [
          { text: "Przewodnik", link: "/pl/get-started.html" },
          { text: "Gospodarki", link: "/pl/economies.html" },
          { text: "Ładunki", link: "/pl/cargos.html" },
          { text: "Branże", link: "/pl/industries.html" },
          { text: "CIRS Growth", link: "/pl/cirs-growth.html" },
          {
            text: "Referencje",
            items: [
              { text: "Dokumentacja kodu", link: "/pl/code-reference.html" },
              { text: "Dziennik zmian", link: "/pl/changelog.html" },
              { text: "Tłumaczenia", link: "/pl/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Przewodnik",
            items: [
              { text: "Rozpocznij", link: "/pl/get-started.html" },
              { text: "Gospodarki", link: "/pl/economies.html" },
              { text: "Ładunki", link: "/pl/cargos.html" },
              { text: "Branże", link: "/pl/industries.html" },
              { text: "CIRS Growth", link: "/pl/cirs-growth.html" }
            ]
          },
          {
            text: "Referencje",
            items: [
              { text: "Dokumentacja kodu", link: "/pl/code-reference.html" },
              { text: "Dziennik zmian", link: "/pl/changelog.html" },
              { text: "Tłumaczenia", link: "/pl/translations.html" }
            ]
          }
        ],
        outline: { label: "Na tej stronie" },
        docFooter: { prev: "Poprzedni", next: "Następny" },
        darkModeSwitchLabel: "Wygląd",
        lightModeSwitchTitle: "Przełącz na jasny motyw",
        darkModeSwitchTitle: "Przełącz na ciemny motyw",
        sidebarMenuLabel: "Menu",
        returnToTopLabel: "Powrót na górę",
        langMenuLabel: "Zmień język",
        externalLinkIcon: true
      }
    },
    'pt-br': {
      label: "Português (BR)",
      lang: "pt-br",
      link: "/pt-br/",
      themeConfig: {
        nav: [
          { text: "Guia", link: "/pt-br/get-started.html" },
          { text: "Economias", link: "/pt-br/economies.html" },
          { text: "Cargas", link: "/pt-br/cargos.html" },
          { text: "Indústrias", link: "/pt-br/industries.html" },
          { text: "CIRS Growth", link: "/pt-br/cirs-growth.html" },
          {
            text: "Referência",
            items: [
              { text: "Referência de código", link: "/pt-br/code-reference.html" },
              { text: "Registro de alterações", link: "/pt-br/changelog.html" },
              { text: "Traduções", link: "/pt-br/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Guia",
            items: [
              { text: "Começar", link: "/pt-br/get-started.html" },
              { text: "Economias", link: "/pt-br/economies.html" },
              { text: "Cargas", link: "/pt-br/cargos.html" },
              { text: "Indústrias", link: "/pt-br/industries.html" },
              { text: "CIRS Growth", link: "/pt-br/cirs-growth.html" }
            ]
          },
          {
            text: "Referência",
            items: [
              { text: "Referência de código", link: "/pt-br/code-reference.html" },
              { text: "Registro de alterações", link: "/pt-br/changelog.html" },
              { text: "Traduções", link: "/pt-br/translations.html" }
            ]
          }
        ],
        outline: { label: "Nesta página" },
        docFooter: { prev: "Anterior", next: "Próximo" },
        darkModeSwitchLabel: "Aparência",
        lightModeSwitchTitle: "Alternar para tema claro",
        darkModeSwitchTitle: "Alternar para tema escuro",
        sidebarMenuLabel: "Menu",
        returnToTopLabel: "Voltar ao topo",
        langMenuLabel: "Alterar idioma",
        externalLinkIcon: true
      }
    },
    'ro': {
      label: "Română",
      lang: "ro",
      link: "/ro/",
      themeConfig: {
        nav: [
          { text: "Ghid", link: "/ro/get-started.html" },
          { text: "Economii", link: "/ro/economies.html" },
          { text: "Mărfuri", link: "/ro/cargos.html" },
          { text: "Industrii", link: "/ro/industries.html" },
          { text: "CIRS Growth", link: "/ro/cirs-growth.html" },
          {
            text: "Referință",
            items: [
              { text: "Referință de cod", link: "/ro/code-reference.html" },
              { text: "Jurnal de modificări", link: "/ro/changelog.html" },
              { text: "Traduceri", link: "/ro/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Ghid",
            items: [
              { text: "Începeți", link: "/ro/get-started.html" },
              { text: "Economii", link: "/ro/economies.html" },
              { text: "Mărfuri", link: "/ro/cargos.html" },
              { text: "Industrii", link: "/ro/industries.html" },
              { text: "CIRS Growth", link: "/ro/cirs-growth.html" }
            ]
          },
          {
            text: "Referință",
            items: [
              { text: "Referință de cod", link: "/ro/code-reference.html" },
              { text: "Jurnal de modificări", link: "/ro/changelog.html" },
              { text: "Traduceri", link: "/ro/translations.html" }
            ]
          }
        ],
        outline: { label: "Pe această pagină" },
        docFooter: { prev: "Precedent", next: "Următor" },
        darkModeSwitchLabel: "Aspect",
        lightModeSwitchTitle: "Comutați la tema deschisă",
        darkModeSwitchTitle: "Comutați la tema închisă",
        sidebarMenuLabel: "Meniu",
        returnToTopLabel: "Înapoi sus",
        langMenuLabel: "Schimbați limba",
        externalLinkIcon: true
      }
    },
    'ru': {
      label: "Русский",
      lang: "ru",
      link: "/ru/",
      themeConfig: {
        nav: [
          { text: "Руководство", link: "/ru/get-started.html" },
          { text: "Экономики", link: "/ru/economies.html" },
          { text: "Грузы", link: "/ru/cargos.html" },
          { text: "Отрасли", link: "/ru/industries.html" },
          { text: "CIRS Growth", link: "/ru/cirs-growth.html" },
          {
            text: "Справочник",
            items: [
              { text: "Справочник по коду", link: "/ru/code-reference.html" },
              { text: "Список изменений", link: "/ru/changelog.html" },
              { text: "Переводы", link: "/ru/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Руководство",
            items: [
              { text: "Начать", link: "/ru/get-started.html" },
              { text: "Экономики", link: "/ru/economies.html" },
              { text: "Грузы", link: "/ru/cargos.html" },
              { text: "Отрасли", link: "/ru/industries.html" },
              { text: "CIRS Growth", link: "/ru/cirs-growth.html" }
            ]
          },
          {
            text: "Справочник",
            items: [
              { text: "Справочник по коду", link: "/ru/code-reference.html" },
              { text: "Список изменений", link: "/ru/changelog.html" },
              { text: "Переводы", link: "/ru/translations.html" }
            ]
          }
        ],
        outline: { label: "На этой странице" },
        docFooter: { prev: "Предыдущая", next: "Следующая" },
        darkModeSwitchLabel: "Внешний вид",
        lightModeSwitchTitle: "Переключить на светлую тему",
        darkModeSwitchTitle: "Переключить на тёмную тему",
        sidebarMenuLabel: "Меню",
        returnToTopLabel: "Вернуться наверх",
        langMenuLabel: "Сменить язык",
        externalLinkIcon: true
      }
    },
    'sk': {
      label: "Slovenčina",
      lang: "sk",
      link: "/sk/",
      themeConfig: {
        nav: [
          { text: "Príručka", link: "/sk/get-started.html" },
          { text: "Ekonomiky", link: "/sk/economies.html" },
          { text: "Náklady", link: "/sk/cargos.html" },
          { text: "Priemyselné odvetvia", link: "/sk/industries.html" },
          { text: "CIRS Growth", link: "/sk/cirs-growth.html" },
          {
            text: "Referencia",
            items: [
              { text: "Referencia kódu", link: "/sk/code-reference.html" },
              { text: "Zoznam zmien", link: "/sk/changelog.html" },
              { text: "Preklady", link: "/sk/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Príručka",
            items: [
              { text: "Začať", link: "/sk/get-started.html" },
              { text: "Ekonomiky", link: "/sk/economies.html" },
              { text: "Náklady", link: "/sk/cargos.html" },
              { text: "Priemyselné odvetvia", link: "/sk/industries.html" },
              { text: "CIRS Growth", link: "/sk/cirs-growth.html" }
            ]
          },
          {
            text: "Referencia",
            items: [
              { text: "Referencia kódu", link: "/sk/code-reference.html" },
              { text: "Zoznam zmien", link: "/sk/changelog.html" },
              { text: "Preklady", link: "/sk/translations.html" }
            ]
          }
        ],
        outline: { label: "Na tejto stránke" },
        docFooter: { prev: "Predchádzajúce", next: "Ďalšie" },
        darkModeSwitchLabel: "Vzhľad",
        lightModeSwitchTitle: "Prepnúť na svetlú tému",
        darkModeSwitchTitle: "Prepnúť na tmavú tému",
        sidebarMenuLabel: "Menu",
        returnToTopLabel: "Návrat hore",
        langMenuLabel: "Zmeniť jazyk",
        externalLinkIcon: true
      }
    },
    'sr': {
      label: "Српски",
      lang: "sr",
      link: "/sr/",
      themeConfig: {
        nav: [
          { text: "Vodič", link: "/sr/get-started.html" },
          { text: "Ekonomije", link: "/sr/economies.html" },
          { text: "Tereti", link: "/sr/cargos.html" },
          { text: "Industrije", link: "/sr/industries.html" },
          { text: "CIRS Growth", link: "/sr/cirs-growth.html" },
          {
            text: "Referenca",
            items: [
              { text: "Referenca koda", link: "/sr/code-reference.html" },
              { text: "Spisak promena", link: "/sr/changelog.html" },
              { text: "Prevodi", link: "/sr/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Vodič",
            items: [
              { text: "Započnite", link: "/sr/get-started.html" },
              { text: "Ekonomije", link: "/sr/economies.html" },
              { text: "Tereti", link: "/sr/cargos.html" },
              { text: "Industrije", link: "/sr/industries.html" },
              { text: "CIRS Growth", link: "/sr/cirs-growth.html" }
            ]
          },
          {
            text: "Referenca",
            items: [
              { text: "Referenca koda", link: "/sr/code-reference.html" },
              { text: "Spisak promena", link: "/sr/changelog.html" },
              { text: "Prevodi", link: "/sr/translations.html" }
            ]
          }
        ],
        outline: { label: "Na ovoj stranici" },
        docFooter: { prev: "Prethodno", next: "Sledeće" },
        darkModeSwitchLabel: "Izgled",
        lightModeSwitchTitle: "Pređite na svetlu temu",
        darkModeSwitchTitle: "Pređite na tamnu temu",
        sidebarMenuLabel: "Meni",
        returnToTopLabel: "Vratite se na vrh",
        langMenuLabel: "Promenite jezik",
        externalLinkIcon: true
      }
    },
    'sv': {
      label: "Svenska",
      lang: "sv",
      link: "/sv/",
      themeConfig: {
        nav: [
          { text: "Guide", link: "/sv/get-started.html" },
          { text: "Ekonomier", link: "/sv/economies.html" },
          { text: "Varor", link: "/sv/cargos.html" },
          { text: "Industrier", link: "/sv/industries.html" },
          { text: "CIRS Growth", link: "/sv/cirs-growth.html" },
          {
            text: "Referens",
            items: [
              { text: "Kodreferens", link: "/sv/code-reference.html" },
              { text: "Ändringslogg", link: "/sv/changelog.html" },
              { text: "Översättningar", link: "/sv/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Guide",
            items: [
              { text: "Kom igång", link: "/sv/get-started.html" },
              { text: "Ekonomier", link: "/sv/economies.html" },
              { text: "Varor", link: "/sv/cargos.html" },
              { text: "Industrier", link: "/sv/industries.html" },
              { text: "CIRS Growth", link: "/sv/cirs-growth.html" }
            ]
          },
          {
            text: "Referens",
            items: [
              { text: "Kodreferens", link: "/sv/code-reference.html" },
              { text: "Ändringslogg", link: "/sv/changelog.html" },
              { text: "Översättningar", link: "/sv/translations.html" }
            ]
          }
        ],
        outline: { label: "På den här sidan" },
        docFooter: { prev: "Föregående", next: "Nästa" },
        darkModeSwitchLabel: "Utseende",
        lightModeSwitchTitle: "Byt till ljust tema",
        darkModeSwitchTitle: "Byt till mörkt tema",
        sidebarMenuLabel: "Meny",
        returnToTopLabel: "Tillbaka till toppen",
        langMenuLabel: "Ändra språk",
        externalLinkIcon: true
      }
    },
    'ta': {
      label: "தமிழ்",
      lang: "ta",
      link: "/ta/",
      themeConfig: {
        nav: [
          { text: "வழிகாட்டி", link: "/ta/get-started.html" },
          { text: "பொருளாதாரங்கள்", link: "/ta/economies.html" },
          { text: "சரக்குகள்", link: "/ta/cargos.html" },
          { text: "தொழில்கள்", link: "/ta/industries.html" },
          { text: "CIRS Growth", link: "/ta/cirs-growth.html" },
          {
            text: "குறிப்பு",
            items: [
              { text: "குறியீட்டுக்கான குறிப்பு", link: "/ta/code-reference.html" },
              { text: "மாற்றப் பதிவு", link: "/ta/changelog.html" },
              { text: "மொழிபெயர்ப்புகள்", link: "/ta/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "வழிகாட்டி",
            items: [
              { text: "தொடங்கவும்", link: "/ta/get-started.html" },
              { text: "பொருளாதாரங்கள்", link: "/ta/economies.html" },
              { text: "சரக்குகள்", link: "/ta/cargos.html" },
              { text: "தொழில்கள்", link: "/ta/industries.html" },
              { text: "CIRS Growth", link: "/ta/cirs-growth.html" }
            ]
          },
          {
            text: "குறிப்பு",
            items: [
              { text: "குறியீட்டுக்கான குறிப்பு", link: "/ta/code-reference.html" },
              { text: "மாற்றப் பதிவு", link: "/ta/changelog.html" },
              { text: "மொழிபெயர்ப்புகள்", link: "/ta/translations.html" }
            ]
          }
        ],
        outline: { label: "இந்தப் பக்கத்தில்" },
        docFooter: { prev: "முந்தைய", next: "அடுத்து" },
        darkModeSwitchLabel: "தோற்றம்",
        lightModeSwitchTitle: "பிரகாசமான தீமுக்கு மாறு",
        darkModeSwitchTitle: "இருண்ட தீமுக்கு மாறு",
        sidebarMenuLabel: "மெனு",
        returnToTopLabel: "மேலே திரும்பு",
        langMenuLabel: "மொழியை மாற்று",
        externalLinkIcon: true
      }
    },
    'tr': {
      label: "Türkçe",
      lang: "tr",
      link: "/tr/",
      themeConfig: {
        nav: [
          { text: "Kılavuz", link: "/tr/get-started.html" },
          { text: "Ekonomiler", link: "/tr/economies.html" },
          { text: "Yükler", link: "/tr/cargos.html" },
          { text: "Endüstriler", link: "/tr/industries.html" },
          { text: "CIRS Growth", link: "/tr/cirs-growth.html" },
          {
            text: "Referans",
            items: [
              { text: "Kod Referansı", link: "/tr/code-reference.html" },
              { text: "Değişiklik Günlüğü", link: "/tr/changelog.html" },
              { text: "Çeviriler", link: "/tr/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "Kılavuz",
            items: [
              { text: "Başlayın", link: "/tr/get-started.html" },
              { text: "Ekonomiler", link: "/tr/economies.html" },
              { text: "Yükler", link: "/tr/cargos.html" },
              { text: "Endüstriler", link: "/tr/industries.html" },
              { text: "CIRS Growth", link: "/tr/cirs-growth.html" }
            ]
          },
          {
            text: "Referans",
            items: [
              { text: "Kod Referansı", link: "/tr/code-reference.html" },
              { text: "Değişiklik Günlüğü", link: "/tr/changelog.html" },
              { text: "Çeviriler", link: "/tr/translations.html" }
            ]
          }
        ],
        outline: { label: "Bu sayfada" },
        docFooter: { prev: "Önceki", next: "Sonraki" },
        darkModeSwitchLabel: "Görünüm",
        lightModeSwitchTitle: "Açık temaya geç",
        darkModeSwitchTitle: "Koyu temaya geç",
        sidebarMenuLabel: "Menü",
        returnToTopLabel: "Başa dön",
        langMenuLabel: "Dili değiştir",
        externalLinkIcon: true
      }
    },
    'zh-hant': {
      label: "繁體中文",
      lang: "zh-hant",
      link: "/zh-hant/",
      themeConfig: {
        nav: [
          { text: "指南", link: "/zh-hant/get-started.html" },
          { text: "經濟", link: "/zh-hant/economies.html" },
          { text: "貨物", link: "/zh-hant/cargos.html" },
          { text: "產業", link: "/zh-hant/industries.html" },
          { text: "CIRS Growth", link: "/zh-hant/cirs-growth.html" },
          {
            text: "參考資料",
            items: [
              { text: "程式碼參考", link: "/zh-hant/code-reference.html" },
              { text: "更新日誌", link: "/zh-hant/changelog.html" },
              { text: "翻譯", link: "/zh-hant/translations.html" }
            ]
          }
        ],
        sidebar: [
          {
            text: "指南",
            items: [
              { text: "開始使用", link: "/zh-hant/get-started.html" },
              { text: "經濟", link: "/zh-hant/economies.html" },
              { text: "貨物", link: "/zh-hant/cargos.html" },
              { text: "產業", link: "/zh-hant/industries.html" },
              { text: "CIRS Growth", link: "/zh-hant/cirs-growth.html" }
            ]
          },
          {
            text: "參考資料",
            items: [
              { text: "程式碼參考", link: "/zh-hant/code-reference.html" },
              { text: "更新日誌", link: "/zh-hant/changelog.html" },
              { text: "翻譯", link: "/zh-hant/translations.html" }
            ]
          }
        ],
        outline: { label: "本頁內容" },
        docFooter: { prev: "上一頁", next: "下一頁" },
        darkModeSwitchLabel: "外觀",
        lightModeSwitchTitle: "切換為淺色主題",
        darkModeSwitchTitle: "切換為深色主題",
        sidebarMenuLabel: "選單",
        returnToTopLabel: "返回頁首",
        langMenuLabel: "更改語言",
        externalLinkIcon: true
      }
    }
  }
})
