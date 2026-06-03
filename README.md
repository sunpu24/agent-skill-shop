# AI Agent Skills 数据可视化作业

这是一个基于 [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) 的数据可视化项目。

项目只保留两个核心能力：

1. **爬取技能列表数据**：从 GitHub README 中解析 skill 名称、描述、链接和分类。
2. **页面展示入口**：保留一个静态跳转页面，后续可接入数据可视化页面。

> 当前项目不会下载任何 skill 仓库，也不会保留本地 skill 文件夹。

## 项目结构

```text
skill-main/
├── config.py              # 爬取地址、数据路径、日志路径配置
├── crawler.py             # 爬虫：读取 README 并解析技能列表
├── data_manager.py        # 数据保存、读取、统计和 CSV 导出
├── main.py                # 命令行入口
├── requirements.txt       # Python 依赖
├── vercel.json            # 静态页面部署配置
├── data/                  # 爬取后生成/保留的数据
└── public/
    └── index.html         # 最终跳转页面
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 爬取数据

```bash
python main.py --crawl
```

生成的数据文件：

```text
data/skills.json
data/skills_summary.json
data/last_update.txt
```

## 查看统计

```bash
python main.py --stats
```

## 导出 CSV

```bash
python main.py --export skills.csv
```

## 页面入口

当前静态入口页面位于：

```text
public/index.html
```

后续可以继续添加数据可视化页面，例如：

```text
public/visualization.html
```

---

# 🤖 Claude Skill Recommendations

## 📚 官方技能来源

本技能商店收录了来自以下顶级团队的官方技能：

- **microsoft** (133个) - [`cloud-solution-architect`](https://officialskills.sh/microsoft/skills/cloud-solution-architect)、[`continual-learning`](https://officialskills.sh/microsoft/skills/continual-learning)、[`copilot-sdk`](https://officialskills.sh/microsoft/skills/copilot-sdk)、[`entra-agent-id`](https://officialskills.sh/microsoft/skills/entra-agent-id)、[`frontend-design-review`](https://officialskills.sh/microsoft/skills/frontend-design-review) 等
- **openai** (42个) - [`cloudflare-deploy`](https://officialskills.sh/openai/skills/cloudflare-deploy)、[`develop-web-game`](https://officialskills.sh/openai/skills/develop-web-game)、[`doc`](https://officialskills.sh/openai/skills/doc)、[`gh-address-comments`](https://officialskills.sh/openai/skills/gh-address-comments)、[`gh-fix-ci`](https://officialskills.sh/openai/skills/gh-fix-ci) 等
- **getsentry** (28个) - [`sentry-sdk-setup`](https://officialskills.sh/getsentry/skills/sentry-sdk-setup)、[`sentry-workflow`](https://officialskills.sh/getsentry/skills/sentry-workflow)、[`sentry-fix-issues`](https://officialskills.sh/getsentry/skills/sentry-fix-issues)、[`sentry-code-review`](https://officialskills.sh/getsentry/skills/sentry-code-review)、[`sentry-pr-code-review`](https://officialskills.sh/getsentry/skills/sentry-pr-code-review) 等
- **garrytan** (27个) - [`office-hours`](https://officialskills.sh/garrytan/skills/office-hours)、[`plan-ceo-review`](https://officialskills.sh/garrytan/skills/plan-ceo-review)、[`plan-eng-review`](https://officialskills.sh/garrytan/skills/plan-eng-review)、[`plan-design-review`](https://officialskills.sh/garrytan/skills/plan-design-review)、[`design-consultation`](https://officialskills.sh/garrytan/skills/design-consultation) 等
- **flutter** (22个) - [`flutter-adding-home-screen-widgets`](https://officialskills.sh/flutter/skills/flutter-adding-home-screen-widgets)、[`flutter-animating-apps`](https://officialskills.sh/flutter/skills/flutter-animating-apps)、[`flutter-architecting-apps`](https://officialskills.sh/flutter/skills/flutter-architecting-apps)、[`flutter-building-forms`](https://officialskills.sh/flutter/skills/flutter-building-forms)、[`flutter-building-layouts`](https://officialskills.sh/flutter/skills/flutter-building-layouts) 等
- **trailofbits** (21个) - [`ask-questions-if-underspecified`](https://officialskills.sh/trailofbits/skills/ask-questions-if-underspecified)、[`audit-context-building`](https://officialskills.sh/trailofbits/skills/audit-context-building)、[`building-secure-contracts`](https://officialskills.sh/trailofbits/skills/building-secure-contracts)、[`burpsuite-project-parser`](https://officialskills.sh/trailofbits/skills/burpsuite-project-parser)、[`claude-in-chrome-troubleshooting`](https://officialskills.sh/trailofbits/skills/claude-in-chrome-troubleshooting) 等
- **anthropics** (17个) - [`docx`](https://officialskills.sh/anthropics/skills/docx)、[`doc-coauthoring`](https://officialskills.sh/anthropics/skills/doc-coauthoring)、[`pptx`](https://officialskills.sh/anthropics/skills/pptx)、[`xlsx`](https://officialskills.sh/anthropics/skills/xlsx)、[`pdf`](https://officialskills.sh/anthropics/skills/pdf) 等
- **googleworkspace** (17个) - [`gws-shared`](https://officialskills.sh/googleworkspace/skills/gws-shared)、[`gws-drive`](https://officialskills.sh/googleworkspace/skills/gws-drive)、[`gws-sheets`](https://officialskills.sh/googleworkspace/skills/gws-sheets)、[`gws-gmail`](https://officialskills.sh/googleworkspace/skills/gws-gmail)、[`gws-calendar`](https://officialskills.sh/googleworkspace/skills/gws-calendar) 等
- **fal-ai-community** (15个) - [`fal-3d`](https://officialskills.sh/fal-ai-community/skills/fal-3d)、[`fal-audio`](https://officialskills.sh/fal-ai-community/skills/fal-audio)、[`fal-generate`](https://officialskills.sh/fal-ai-community/skills/fal-generate)、[`fal-image-edit`](https://officialskills.sh/fal-ai-community/skills/fal-image-edit)、[`fal-kling-o3`](https://officialskills.sh/fal-ai-community/skills/fal-kling-o3) 等
- **auth0** (14个) - [`auth0-android`](https://officialskills.sh/auth0/skills/auth0-android)、[`auth0-angular`](https://officialskills.sh/auth0/skills/auth0-angular)、[`auth0-aspnetcore-api`](https://officialskills.sh/auth0/skills/auth0-aspnetcore-api)、[`auth0-express`](https://officialskills.sh/auth0/skills/auth0-express)、[`auth0-fastify`](https://officialskills.sh/auth0/skills/auth0-fastify) 等
- **huggingface** (13个) - [`hf-cli`](https://officialskills.sh/huggingface/skills/hf-cli)、[`hugging-face-dataset-viewer`](https://officialskills.sh/huggingface/skills/hugging-face-dataset-viewer)、[`hugging-face-datasets`](https://officialskills.sh/huggingface/skills/hugging-face-datasets)、[`hugging-face-evaluation`](https://officialskills.sh/huggingface/skills/hugging-face-evaluation)、[`hugging-face-jobs`](https://officialskills.sh/huggingface/skills/hugging-face-jobs) 等
- **WordPress** (13个) - [`wordpress-router`](https://officialskills.sh/WordPress/skills/wordpress-router)、[`wp-project-triage`](https://officialskills.sh/WordPress/skills/wp-project-triage)、[`wp-block-development`](https://officialskills.sh/WordPress/skills/wp-block-development)、[`wp-block-themes`](https://officialskills.sh/WordPress/skills/wp-block-themes)、[`wp-plugin-development`](https://officialskills.sh/WordPress/skills/wp-plugin-development) 等
- **apollographql** (13个) - [`apollo-client`](https://officialskills.sh/apollographql/skills/apollo-client)、[`apollo-connectors`](https://officialskills.sh/apollographql/skills/apollo-connectors)、[`apollo-federation`](https://officialskills.sh/apollographql/skills/apollo-federation)、[`apollo-kotlin`](https://officialskills.sh/apollographql/skills/apollo-kotlin)、[`apollo-mcp-server`](https://officialskills.sh/apollographql/skills/apollo-mcp-server) 等
- **netlify** (12个) - [`netlify-functions`](https://officialskills.sh/netlify/skills/netlify-functions)、[`netlify-edge-functions`](https://officialskills.sh/netlify/skills/netlify-edge-functions)、[`netlify-blobs`](https://officialskills.sh/netlify/skills/netlify-blobs)、[`netlify-db`](https://officialskills.sh/netlify/skills/netlify-db)、[`netlify-image-cdn`](https://officialskills.sh/netlify/skills/netlify-image-cdn) 等
- **firebase** (12个) - [`developing-genkit-dart`](https://officialskills.sh/firebase/skills/developing-genkit-dart)、[`developing-genkit-go`](https://officialskills.sh/firebase/skills/developing-genkit-go)、[`developing-genkit-js`](https://officialskills.sh/firebase/skills/developing-genkit-js)、[`firebase-ai-logic-basics`](https://officialskills.sh/firebase/skills/firebase-ai-logic-basics)、[`firebase-app-hosting-basics`](https://officialskills.sh/firebase/skills/firebase-app-hosting-basics) 等
- **hashicorp** (11个) - [`azure-verified-modules`](https://officialskills.sh/hashicorp/skills/azure-verified-modules)、[`new-terraform-provider`](https://officialskills.sh/hashicorp/skills/new-terraform-provider)、[`provider-resources`](https://officialskills.sh/hashicorp/skills/provider-resources)、[`provider-test-patterns`](https://officialskills.sh/hashicorp/skills/provider-test-patterns)、[`provider-actions`](https://officialskills.sh/hashicorp/skills/provider-actions) 等
- **expo** (11个) - [`building-native-ui`](https://officialskills.sh/expo/skills/building-native-ui)、[`expo-api-routes`](https://officialskills.sh/expo/skills/expo-api-routes)、[`expo-cicd-workflows`](https://officialskills.sh/expo/skills/expo-cicd-workflows)、[`expo-deployment`](https://officialskills.sh/expo/skills/expo-deployment)、[`expo-dev-client`](https://officialskills.sh/expo/skills/expo-dev-client) 等
- **brave** (11个) - [`answers`](https://officialskills.sh/brave/skills/answers)、[`bx`](https://officialskills.sh/brave/skills/bx)、[`images-search`](https://officialskills.sh/brave/skills/images-search)、[`llm-context`](https://officialskills.sh/brave/skills/llm-context)、[`local-descriptions`](https://officialskills.sh/brave/skills/local-descriptions) 等
- **MiniMax-AI** (11个) - [`cli`](https://officialskills.sh/MiniMax-AI/skills/cli)、[`frontend-dev`](https://officialskills.sh/MiniMax-AI/skills/frontend-dev)、[`fullstack-dev`](https://officialskills.sh/MiniMax-AI/skills/fullstack-dev)、[`android-native-dev`](https://officialskills.sh/MiniMax-AI/skills/android-native-dev)、[`ios-application-dev`](https://officialskills.sh/MiniMax-AI/skills/ios-application-dev) 等
- **coinbase** (9个) - [`authenticate-wallet`](https://officialskills.sh/coinbase/skills/authenticate-wallet)、[`fund`](https://officialskills.sh/coinbase/skills/fund)、[`monetize-service`](https://officialskills.sh/coinbase/skills/monetize-service)、[`pay-for-service`](https://officialskills.sh/coinbase/skills/pay-for-service)、[`query-onchain-data`](https://officialskills.sh/coinbase/skills/query-onchain-data) 等
- **cloudflare** (8个) - [`agents-sdk`](https://officialskills.sh/cloudflare/skills/agents-sdk)、[`cloudflare`](https://officialskills.sh/cloudflare/skills/cloudflare)、[`cloudflare-email-service`](https://officialskills.sh/cloudflare/skills/cloudflare-email-service)、[`durable-objects`](https://officialskills.sh/cloudflare/skills/durable-objects)、[`sandbox-sdk`](https://officialskills.sh/cloudflare/skills/sandbox-sdk) 等
- **datadog-labs** (8个) - [`dd-apm`](https://officialskills.sh/datadog-labs/skills/dd-apm)、[`dd-docs`](https://officialskills.sh/datadog-labs/skills/dd-docs)、[`dd-llmo-eval-bootstrap`](https://officialskills.sh/datadog-labs/skills/dd-llmo-eval-bootstrap)、[`dd-llmo-eval-trace-rca`](https://officialskills.sh/datadog-labs/skills/dd-llmo-eval-trace-rca)、[`dd-llmo-experiment-analyzer`](https://officialskills.sh/datadog-labs/skills/dd-llmo-experiment-analyzer) 等
- **greensock** (8个) - [`gsap-core`](https://officialskills.sh/greensock/skills/gsap-core)、[`gsap-timeline`](https://officialskills.sh/greensock/skills/gsap-timeline)、[`gsap-scrolltrigger`](https://officialskills.sh/greensock/skills/gsap-scrolltrigger)、[`gsap-plugins`](https://officialskills.sh/greensock/skills/gsap-plugins)、[`gsap-utils`](https://officialskills.sh/greensock/skills/gsap-utils) 等
- **makenotion** (8个) - [`knowledge-capture`](https://officialskills.sh/makenotion/skills/knowledge-capture)、[`meeting-intelligence`](https://officialskills.sh/makenotion/skills/meeting-intelligence)、[`research-documentation`](https://officialskills.sh/makenotion/skills/research-documentation)、[`spec-to-implementation`](https://officialskills.sh/makenotion/skills/spec-to-implementation)、[`knowledge-capture`](https://officialskills.sh/makenotion/skills/knowledge-capture) 等
- **better-auth** (7个) - [`best-practices`](https://officialskills.sh/better-auth/skills/best-practices)、[`explain-error`](https://officialskills.sh/better-auth/skills/explain-error)、[`providers`](https://officialskills.sh/better-auth/skills/providers)、[`create-auth`](https://officialskills.sh/better-auth/skills/create-auth)、[`emailAndPassword`](https://officialskills.sh/better-auth/skills/emailAndPassword) 等
- **vercel-labs** (7个) - [`react-best-practices`](https://officialskills.sh/vercel-labs/skills/react-best-practices)、[`web-design-guidelines`](https://officialskills.sh/vercel-labs/skills/web-design-guidelines)、[`composition-patterns`](https://officialskills.sh/vercel-labs/skills/composition-patterns)、[`next-best-practices`](https://officialskills.sh/vercel-labs/skills/next-best-practices)、[`next-cache-components`](https://officialskills.sh/vercel-labs/skills/next-cache-components) 等
- **figma** (7个) - [`figma-code-connect-components`](https://officialskills.sh/figma/skills/figma-code-connect-components)、[`figma-create-design-system-rules`](https://officialskills.sh/figma/skills/figma-create-design-system-rules)、[`figma-create-new-file`](https://officialskills.sh/figma/skills/figma-create-new-file)、[`figma-generate-design`](https://officialskills.sh/figma/skills/figma-generate-design)、[`figma-generate-library`](https://officialskills.sh/figma/skills/figma-generate-library) 等
- **binance** (7个) - [`crypto-market-rank`](https://officialskills.sh/binance/skills/crypto-market-rank)、[`meme-rush`](https://officialskills.sh/binance/skills/meme-rush)、[`query-address-info`](https://officialskills.sh/binance/skills/query-address-info)、[`query-token-audit`](https://officialskills.sh/binance/skills/query-token-audit)、[`query-token-info`](https://officialskills.sh/binance/skills/query-token-info) 等
- **browserbase** (7个) - [`browser`](https://officialskills.sh/browserbase/skills/browser)、[`browserbase-cli`](https://officialskills.sh/browserbase/skills/browserbase-cli)、[`cookie-sync`](https://officialskills.sh/browserbase/skills/cookie-sync)、[`fetch`](https://officialskills.sh/browserbase/skills/fetch)、[`functions`](https://officialskills.sh/browserbase/skills/functions) 等
- **mongodb** (7个) - [`mongodb-mcp-setup`](https://officialskills.sh/mongodb/skills/mongodb-mcp-setup)、[`mongodb-connection`](https://officialskills.sh/mongodb/skills/mongodb-connection)、[`mongodb-schema-design`](https://officialskills.sh/mongodb/skills/mongodb-schema-design)、[`atlas-stream-processing`](https://officialskills.sh/mongodb/skills/atlas-stream-processing)、[`mongodb-natural-language-querying`](https://officialskills.sh/mongodb/skills/mongodb-natural-language-querying) 等
- **clickhouse** (6个) - [`clickhouse-best-practices`](https://officialskills.sh/clickhouse/skills/clickhouse-best-practices)、[`chdb-datastore`](https://officialskills.sh/clickhouse/skills/chdb-datastore)、[`chdb-sql`](https://officialskills.sh/clickhouse/skills/chdb-sql)、[`clickhouse-architecture-advisor`](https://officialskills.sh/clickhouse/skills/clickhouse-architecture-advisor)、[`clickhousectl-cloud-deploy`](https://officialskills.sh/clickhouse/skills/clickhousectl-cloud-deploy) 等
- **google-labs-code** (6个) - [`design-md`](https://officialskills.sh/google-labs-code/skills/design-md)、[`enhance-prompt`](https://officialskills.sh/google-labs-code/skills/enhance-prompt)、[`react-components`](https://officialskills.sh/google-labs-code/skills/react-components)、[`remotion`](https://officialskills.sh/google-labs-code/skills/remotion)、[`shadcn-ui`](https://officialskills.sh/google-labs-code/skills/shadcn-ui) 等
- **duckdb** (6个) - [`attach-db`](https://officialskills.sh/duckdb/skills/attach-db)、[`query`](https://officialskills.sh/duckdb/skills/query)、[`read-file`](https://officialskills.sh/duckdb/skills/read-file)、[`duckdb-docs`](https://officialskills.sh/duckdb/skills/duckdb-docs)、[`read-memories`](https://officialskills.sh/duckdb/skills/read-memories) 等
- **addyosmani** (6个) - [`web-quality-audit`](https://officialskills.sh/addyosmani/skills/web-quality-audit)、[`performance`](https://officialskills.sh/addyosmani/skills/performance)、[`core-web-vitals`](https://officialskills.sh/addyosmani/skills/core-web-vitals)、[`accessibility`](https://officialskills.sh/addyosmani/skills/accessibility)、[`seo`](https://officialskills.sh/addyosmani/skills/seo) 等
- **firecrawl** (5个) - [`firecrawl-build`](https://officialskills.sh/firecrawl/skills/firecrawl-build)、[`firecrawl-build-interact`](https://officialskills.sh/firecrawl/skills/firecrawl-build-interact)、[`firecrawl-build-onboarding`](https://officialskills.sh/firecrawl/skills/firecrawl-build-onboarding)、[`firecrawl-build-scrape`](https://officialskills.sh/firecrawl/skills/firecrawl-build-scrape)、[`firecrawl-build-search`](https://officialskills.sh/firecrawl/skills/firecrawl-build-search)
- **voltagent** (4个) - [`create-voltagent`](https://officialskills.sh/voltagent/skills/create-voltagent)、[`voltagent-best-practices`](https://officialskills.sh/voltagent/skills/voltagent-best-practices)、[`voltagent-core-reference`](https://officialskills.sh/voltagent/skills/voltagent-core-reference)、[`voltagent-docs-bundle`](https://officialskills.sh/voltagent/skills/voltagent-docs-bundle)
- **google-gemini** (4个) - [`gemini-api-dev`](https://officialskills.sh/google-gemini/skills/gemini-api-dev)、[`vertex-ai-api-dev`](https://officialskills.sh/google-gemini/skills/vertex-ai-api-dev)、[`gemini-live-api-dev`](https://officialskills.sh/google-gemini/skills/gemini-live-api-dev)、[`gemini-interactions-api`](https://officialskills.sh/google-gemini/skills/gemini-interactions-api)
- **tinybirdco** (4个) - [`tinybird-best-practices`](https://officialskills.sh/tinybirdco/skills/tinybird-best-practices)、[`tinybird-cli-guidelines`](https://officialskills.sh/tinybirdco/skills/tinybird-cli-guidelines)、[`tinybird-python-sdk-guidelines`](https://officialskills.sh/tinybirdco/skills/tinybird-python-sdk-guidelines)、[`tinybird-typescript-sdk-guidelines`](https://officialskills.sh/tinybirdco/skills/tinybird-typescript-sdk-guidelines)
- **sanity-io** (4个) - [`sanity-best-practices`](https://officialskills.sh/sanity-io/skills/sanity-best-practices)、[`content-modeling-best-practices`](https://officialskills.sh/sanity-io/skills/content-modeling-best-practices)、[`seo-aeo-best-practices`](https://officialskills.sh/sanity-io/skills/seo-aeo-best-practices)、[`content-experimentation-best-practices`](https://officialskills.sh/sanity-io/skills/content-experimentation-best-practices)
- **callstackincubator** (3个) - [`react-native-best-practices`](https://officialskills.sh/callstackincubator/skills/react-native-best-practices)、[`github`](https://officialskills.sh/callstackincubator/skills/github)、[`upgrading-react-native`](https://officialskills.sh/callstackincubator/skills/upgrading-react-native)
- **neondatabase** (3个) - [`neon-postgres`](https://officialskills.sh/neondatabase/skills/neon-postgres)、[`claimable-postgres`](https://officialskills.sh/neondatabase/skills/claimable-postgres)、[`neon-postgres-egress-optimizer`](https://officialskills.sh/neondatabase/skills/neon-postgres-egress-optimizer)
- **stripe** (2个) - [`stripe-best-practices`](https://officialskills.sh/stripe/skills/stripe-best-practices)、[`upgrade-stripe`](https://officialskills.sh/stripe/skills/upgrade-stripe)
- **coderabbitai** (2个) - [`autofix`](https://officialskills.sh/coderabbitai/skills/autofix)、[`code-review`](https://officialskills.sh/coderabbitai/skills/code-review)
- **composiohq** (1个) - [`composio`](https://officialskills.sh/composiohq/skills/composio)
- **supabase** (1个) - [`postgres-best-practices`](https://officialskills.sh/supabase/skills/postgres-best-practices)
- **remotion-dev** (1个) - [`remotion`](https://officialskills.sh/remotion-dev/skills/remotion)
- **replicate** (1个) - [`replicate`](https://officialskills.sh/replicate/skills/replicate)
- **typefully** (1个) - [`typefully`](https://officialskills.sh/typefully/skills/typefully)

## 💾 社区技能库

### 网络安全（23个）

- [mukul975/Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) ⭐⭐⭐⭐⭐ 夯 - 安全审计与漏洞防护
- [prompt-security/clawsec](https://github.com/prompt-security/clawsec) ⭐⭐⭐⭐⭐ 夯 - 安全审计与漏洞防护
- [google/cloud/google-cloud-waf-security](https://github.com/google/skills/tree/main/skills/cloud/google-cloud-waf-security) ⭐⭐⭐⭐⭐ 夯 - 安全审计与漏洞防护
- [NeoLabHQ/code-review](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/code-review) ⭐⭐⭐⭐⭐ 夯 - 安全审计与漏洞防护
- [obra/defense-in-depth](https://github.com/obra/superpowers/blob/main/skills/defense-in-depth/SKILL.md) ⭐⭐⭐⭐⭐ 夯 - 安全审计与漏洞防护

### 法律合同（27个）

- [phuryn/privacy-policy](https://github.com/phuryn/pm-skills/tree/main/pm-toolkit/skills/privacy-policy) ⭐⭐⭐⭐⭐ 夯 - 法律合规与政策文档处理
- [phuryn/pestle-analysis](https://github.com/phuryn/pm-skills/tree/main/pm-product-strategy/skills/pestle-analysis) ⭐⭐⭐⭐ 顶级 - 法律合规与政策文档处理
- [NVIDIA/NemoClaw/nemoclaw-user-manage-policy](https://github.com/NVIDIA/skills/tree/main/skills/NemoClaw/nemoclaw-user-manage-policy) ⭐⭐⭐⭐ 顶级 - 大模型系统策略管理与合规控制
- [deanpeters/pestel-analysis](https://github.com/deanpeters/Product-Manager-Skills/tree/main/skills/pestel-analysis) ⭐⭐⭐⭐ 顶级 - 法律合规与政策文档处理
- [deanpeters/epic-breakdown-advisor](https://github.com/deanpeters/Product-Manager-Skills/tree/main/skills/epic-breakdown-advisor) ⭐⭐⭐⭐ 顶级 - 法律合规与政策文档处理

### 金融分析（17个）

- [deanpeters/finance-based-pricing-advisor](https://github.com/deanpeters/Product-Manager-Skills/tree/main/skills/finance-based-pricing-advisor) ⭐⭐⭐⭐⭐ 夯 - 财务分析与商业决策
- [coreyhaines31/pricing-strategy](https://github.com/coreyhaines31/marketingskills/tree/main/skills/pricing-strategy) ⭐⭐⭐⭐⭐ 夯 - 财务分析与商业决策
- [phuryn/business-model](https://github.com/phuryn/pm-skills/tree/main/pm-product-strategy/skills/business-model) ⭐⭐⭐⭐⭐ 夯 - 财务分析与商业决策
- [deanpeters/business-health-diagnostic](https://github.com/deanpeters/Product-Manager-Skills/tree/main/skills/business-health-diagnostic) ⭐⭐⭐⭐⭐ 夯 - 商业健康度诊断与经营分析
- [deanpeters/finance-metrics-quickref](https://github.com/deanpeters/Product-Manager-Skills/tree/main/skills/finance-metrics-quickref) ⭐⭐⭐⭐⭐ 夯 - 财务分析与商业决策

### 教育学习（10个）

- [santifer/career-ops](https://github.com/santifer/career-ops) ⭐⭐⭐⭐⭐ 夯 - 面试准备与访谈整理
- [Paramchoudhary/ResumeSkills](https://github.com/Paramchoudhary/ResumeSkills) ⭐⭐⭐⭐⭐ 夯 - 简历优化与求职准备
- [phuryn/interview-script](https://github.com/phuryn/pm-skills/tree/main/pm-product-discovery/skills/interview-script) ⭐⭐⭐⭐ 顶级 - 面试准备与访谈整理

### 医疗健康（5个）

- [zw008/VMware-AIops](https://github.com/zw008/VMware-AIops) ⭐⭐⭐⭐ 顶级 - 健康信息分析与系统监测
- [huifer/Claude-Ally-Health](https://github.com/huifer/Claude-Ally-Health) ⭐⭐⭐⭐ 顶级 - 健康信息分析与系统监测
- [foryourhealth111-pixel/Vibe-Skills](https://github.com/foryourhealth111-pixel/Vibe-Skills) ⭐⭐⭐⭐ 顶级 - 健康信息分析与系统监测

### 科研论文（28个）

- [deanpeters/proto-persona](https://github.com/deanpeters/Product-Manager-Skills/tree/main/skills/proto-persona) ⭐⭐⭐⭐⭐ 夯 - 研究调研与资料分析
- [K-Dense-AI/claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills) ⭐⭐⭐⭐⭐ 夯 - 科研资料分析
- [Orchestra-Research/AI-research-SKILLs](https://github.com/Orchestra-Research/AI-research-SKILLs) ⭐⭐⭐⭐⭐ 夯 - 科研论文分析
- [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) ⭐⭐⭐⭐⭐ 夯 - 研究调研与资料分析
- [wanshuiyin/Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) ⭐⭐⭐⭐⭐ 夯 - 研究调研与资料分析

### 电商零售（15个）

- [coreyhaines31/product-marketing-context](https://github.com/coreyhaines31/marketingskills/tree/main/skills/product-marketing-context) ⭐⭐⭐⭐ 顶级 - 产品营销与转化优化
- [coreyhaines31/sales-enablement](https://github.com/coreyhaines31/marketingskills/tree/main/skills/sales-enablement) ⭐⭐⭐⭐ 顶级 - 销售转化与客户运营
- [phuryn/competitive-battlecard](https://github.com/phuryn/pm-skills/tree/main/pm-go-to-market/skills/competitive-battlecard) ⭐⭐⭐⭐ 顶级 - 销售转化与客户运营
- [phuryn/value-prop-statements](https://github.com/phuryn/pm-skills/tree/main/pm-marketing-growth/skills/value-prop-statements) ⭐⭐⭐⭐ 顶级 - 销售转化与客户运营
- [phuryn/customer-journey-map](https://github.com/phuryn/pm-skills/tree/main/pm-market-research/skills/customer-journey-map) ⭐⭐⭐⭐ 顶级 - 电商运营与商品营销

### 增长广告（26个）

- [coreyhaines31/competitor-alternatives](https://github.com/coreyhaines31/marketingskills/tree/main/skills/competitor-alternatives) ⭐⭐⭐⭐⭐ 夯 - 网站搜索优化与增长分析
- [coreyhaines31/copywriting](https://github.com/coreyhaines31/marketingskills/tree/main/skills/copywriting) ⭐⭐⭐⭐⭐ 夯 - 写作辅助与文本优化
- [coreyhaines31/page-cro](https://github.com/coreyhaines31/marketingskills/tree/main/skills/page-cro) ⭐⭐⭐⭐⭐ 夯 - 搜索优化、增长与广告投放
- [coreyhaines31/ai-seo](https://github.com/coreyhaines31/marketingskills/tree/main/skills/ai-seo) ⭐⭐⭐⭐⭐ 夯 - 网站搜索优化与增长分析
- [coreyhaines31/paid-ads](https://github.com/coreyhaines31/marketingskills/tree/main/skills/paid-ads) ⭐⭐⭐⭐⭐ 夯 - 搜索优化、增长与广告投放

### 社媒运营（17个）

- [coreyhaines31/social-content](https://github.com/coreyhaines31/marketingskills/tree/main/skills/social-content) ⭐⭐⭐⭐⭐ 夯 - 社交平台内容发布与运营
- [coreyhaines31/onboarding-cro](https://github.com/coreyhaines31/marketingskills/tree/main/skills/onboarding-cro) ⭐⭐⭐⭐ 顶级 - 社媒内容运营与发布
- [Xquik-dev/x-twitter-scraper](https://github.com/Xquik-dev/x-twitter-scraper) ⭐⭐⭐⭐ 顶级 - 社交平台内容发布与运营
- [NVIDIA/TensorRT-LLM/ad-accuracy-debug](https://github.com/NVIDIA/skills/tree/main/skills/TensorRT-LLM/ad-accuracy-debug) ⭐⭐⭐⭐ 顶级 - 大语言模型训练、推理或评估
- [NVIDIA/video-search-and-summarization/report](https://github.com/NVIDIA/skills/tree/main/skills/video-search-and-summarization/report) ⭐⭐⭐⭐ 顶级 - 视频生成、理解或处理

### 邮件营销（13个）

- [coreyhaines31/cold-email](https://github.com/coreyhaines31/marketingskills/tree/main/skills/cold-email) ⭐⭐⭐⭐⭐ 夯 - 邮件营销与用户触达
- [coreyhaines31/email-sequence](https://github.com/coreyhaines31/marketingskills/tree/main/skills/email-sequence) ⭐⭐⭐⭐⭐ 夯 - 邮件营销与用户触达
- [phuryn/outcome-roadmap](https://github.com/phuryn/pm-skills/tree/main/pm-execution/skills/outcome-roadmap) ⭐⭐⭐⭐ 顶级 - 邮件营销与用户触达
- [deanpeters/eol-message](https://github.com/deanpeters/Product-Manager-Skills/tree/main/skills/eol-message) ⭐⭐⭐⭐ 顶级 - 邮件营销与用户触达
- [deanpeters/product-strategy-session](https://github.com/deanpeters/Product-Manager-Skills/tree/main/skills/product-strategy-session) ⭐⭐⭐⭐ 顶级 - 邮件营销与用户触达

### 视频创作（35个）

- [NVIDIA/video-search-and-summarization/vios](https://github.com/NVIDIA/skills/tree/main/skills/video-search-and-summarization/vios) ⭐⭐⭐⭐⭐ 夯 - 视频生成、理解或处理
- [google/cloud/agent-platform-skill-registry](https://github.com/google/skills/tree/main/skills/cloud/agent-platform-skill-registry) ⭐⭐⭐⭐⭐ 夯 - 智能体工作流与任务协作
- [NVIDIA/video-search-and-summarization/alerts](https://github.com/NVIDIA/skills/tree/main/skills/video-search-and-summarization/alerts) ⭐⭐⭐⭐⭐ 夯 - 视频生成、理解或处理
- [NVIDIA/video-search-and-summarization/deploy](https://github.com/NVIDIA/skills/tree/main/skills/video-search-and-summarization/deploy) ⭐⭐⭐⭐⭐ 夯 - 视频生成、理解或处理
- [NVIDIA/video-search-and-summarization/vss-frag](https://github.com/NVIDIA/skills/tree/main/skills/video-search-and-summarization/vss-frag) ⭐⭐⭐⭐⭐ 夯 - 视频生成、理解或处理
- [google/cloud/cloud-sql-basics](https://github.com/google/skills/tree/main/skills/cloud/cloud-sql-basics) ⭐⭐⭐⭐⭐ 夯 - 视频创作、理解与处理
- [google/cloud/gke-basics](https://github.com/google/skills/tree/main/skills/cloud/gke-basics) ⭐⭐⭐⭐⭐ 夯 - 视频创作、理解与处理
- [google/cloud/google-cloud-recipe-onboarding](https://github.com/google/skills/tree/main/skills/cloud/google-cloud-recipe-onboarding) ⭐⭐⭐⭐⭐ 夯 - 视频创作、理解与处理

### 图片生成（5个）

- [sanjay3290/imagen](https://github.com/sanjay3290/ai-skills/tree/main/skills/imagen) ⭐⭐⭐⭐⭐ 夯 - 图片生成与编辑
- [veniceai/venice-image-edit](https://github.com/veniceai/skills/tree/main/skills/venice-image-edit) ⭐⭐⭐⭐ 顶级 - 图片生成与编辑
- [NVIDIA/Megatron-Core/bump-base-image](https://github.com/NVIDIA/skills/tree/main/skills/Megatron-Core/bump-base-image) ⭐⭐⭐⭐ 顶级 - 图片生成与编辑

### 语音音频（7个）

- [blader/humanizer](https://github.com/blader/humanizer) ⭐⭐⭐⭐ 顶级 - 写作辅助与文本优化
- [veniceai/venice-audio-speech](https://github.com/veniceai/skills/tree/main/skills/venice-audio-speech) ⭐⭐⭐⭐ 顶级 - 音频生成、转录或处理
- [NVIDIA/nemotron-voice-agent/nemotron-voice-agent-deploy](https://github.com/NVIDIA/skills/tree/main/skills/nemotron-voice-agent/nemotron-voice-agent-deploy) ⭐⭐⭐⭐ 顶级 - 语音合成与语音代理

### 写作文案（13个）

- [NeoLabHQ/write-concisely](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/docs/skills/write-concisely) ⭐⭐⭐⭐⭐ 夯 - 写作辅助与文本优化
- [coreyhaines31/copy-editing](https://github.com/coreyhaines31/marketingskills/tree/main/skills/copy-editing) ⭐⭐⭐⭐ 顶级 - 写作辅助与文本优化
- [obra/writing-plans](https://github.com/obra/superpowers/blob/main/skills/writing-plans/SKILL.md) ⭐⭐⭐⭐ 顶级 - 写作辅助与文本优化
- [coreyhaines31/content-strategy](https://github.com/coreyhaines31/marketingskills/tree/main/skills/content-strategy) ⭐⭐⭐⭐ 顶级 - 写作辅助与文本优化
- [NVIDIA/TensorRT-LLM/kernel-cute-writing](https://github.com/NVIDIA/skills/tree/main/skills/TensorRT-LLM/kernel-cute-writing) ⭐⭐⭐⭐ 顶级 - 写作辅助与文本优化

### 办公文档（19个）

- [Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) ⭐⭐⭐⭐⭐ 夯 - PDF 文档处理与转换
- [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides) ⭐⭐⭐⭐⭐ 夯 - 演示文稿生成与美化
- [kreuzberg-dev/kreuzberg](https://github.com/kreuzberg-dev/kreuzberg/tree/main/skills/kreuzberg) ⭐⭐⭐⭐⭐ 夯 - 文档处理与知识整理
- [deanpeters/recommendation-canvas](https://github.com/deanpeters/Product-Manager-Skills/tree/main/skills/recommendation-canvas) ⭐⭐⭐⭐⭐ 夯 - 文档处理与知识整理
- [NVIDIA/NeMo-Gym/nemo-gym-pivot-datasets](https://github.com/NVIDIA/skills/tree/main/skills/NeMo-Gym/nemo-gym-pivot-datasets) ⭐⭐⭐⭐ 顶级 - 文档处理与知识整理

### 界面设计（43个）

- [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) ⭐⭐⭐⭐⭐ 夯 - 界面设计与用户体验优化
- [coreyhaines31/churn-prevention](https://github.com/coreyhaines31/marketingskills/tree/main/skills/churn-prevention) ⭐⭐⭐⭐ 顶级 - 界面设计与用户体验优化
- [phuryn/stakeholder-map](https://github.com/phuryn/pm-skills/tree/main/pm-execution/skills/stakeholder-map) ⭐⭐⭐⭐ 顶级 - 界面设计与用户体验优化
- [phuryn/opportunity-solution-tree](https://github.com/phuryn/pm-skills/tree/main/pm-product-discovery/skills/opportunity-solution-tree) ⭐⭐⭐⭐ 顶级 - 界面设计与用户体验优化
- [muratcankoylan/tool-design](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/tree/main/skills/tool-design) ⭐⭐⭐⭐ 顶级 - 智能体工作流与任务协作
- [czlonkowski/n8n-mcp-tools-expert](https://github.com/czlonkowski/n8n-skills/tree/main/skills/n8n-mcp-tools-expert) ⭐⭐⭐⭐ 顶级 - 工具协议集成与自动化
- [NVIDIA/TensorRT-LLM/ad-model-onboard](https://github.com/NVIDIA/skills/tree/main/skills/TensorRT-LLM/ad-model-onboard) ⭐⭐⭐⭐ 顶级 - 大语言模型训练、推理或评估
- [NVIDIA/cuopt/cuopt-developer](https://github.com/NVIDIA/skills/tree/main/skills/cuopt/cuopt-developer) ⭐⭐⭐⭐ 顶级 - 编程开发辅助

### 编程开发（111个）

- [czlonkowski/n8n-code-python](https://github.com/czlonkowski/n8n-skills/tree/main/skills/n8n-code-python) ⭐⭐⭐⭐⭐ 夯 - 编程开发辅助
- [NVIDIA/deepstream/deepstream-dev](https://github.com/NVIDIA/skills/tree/main/skills/deepstream/deepstream-dev) ⭐⭐⭐⭐⭐ 夯 - 编程开发辅助
- [czlonkowski/n8n-code-javascript](https://github.com/czlonkowski/n8n-skills/tree/main/skills/n8n-code-javascript) ⭐⭐⭐⭐⭐ 夯 - 编程开发与框架实践
- [NeoLabHQ/sadd](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/sadd) ⭐⭐⭐⭐⭐ 夯 - 智能体工作流与任务协作
- [coreyhaines31/ad-creative](https://github.com/coreyhaines31/marketingskills/tree/main/skills/ad-creative) ⭐⭐⭐⭐ 顶级 - 编程开发与框架实践
- [coreyhaines31/paywall-upgrade-cro](https://github.com/coreyhaines31/marketingskills/tree/main/skills/paywall-upgrade-cro) ⭐⭐⭐⭐ 顶级 - 编程开发与框架实践
- [coreyhaines31/referral-program](https://github.com/coreyhaines31/marketingskills/tree/main/skills/referral-program) ⭐⭐⭐⭐ 顶级 - 编程开发与框架实践
- [phuryn/ab-test-analysis](https://github.com/phuryn/pm-skills/tree/main/pm-data-analytics/skills/ab-test-analysis) ⭐⭐⭐⭐ 顶级 - 编程开发与框架实践
- [phuryn/sql-queries](https://github.com/phuryn/pm-skills/tree/main/pm-data-analytics/skills/sql-queries) ⭐⭐⭐⭐ 顶级 - 编程开发与框架实践
- [phuryn/create-prd](https://github.com/phuryn/pm-skills/tree/main/pm-execution/skills/create-prd) ⭐⭐⭐⭐ 顶级 - 编程开发与框架实践

### 自动工作流（17个）

- [czlonkowski/n8n-workflow-patterns](https://github.com/czlonkowski/n8n-skills/tree/main/skills/n8n-workflow-patterns) ⭐⭐⭐⭐⭐ 夯 - 自动化工作流搭建
- [czlonkowski/n8n-expression-syntax](https://github.com/czlonkowski/n8n-skills/tree/main/skills/n8n-expression-syntax) ⭐⭐⭐⭐ 顶级 - 自动化工作流与工具集成
- [czlonkowski/n8n-node-configuration](https://github.com/czlonkowski/n8n-skills/tree/main/skills/n8n-node-configuration) ⭐⭐⭐⭐ 顶级 - 自动化工作流与工具集成
- [czlonkowski/n8n-validation-expert](https://github.com/czlonkowski/n8n-skills/tree/main/skills/n8n-validation-expert) ⭐⭐⭐⭐ 顶级 - 自动化工作流与工具集成
- [Charlie85270/Dorothy](https://github.com/Charlie85270/Dorothy) ⭐⭐⭐⭐ 顶级 - 智能体工作流与任务协作

### 提示工程（53个）

- [muratcankoylan/context-fundamentals](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/tree/main/skills/context-fundamentals) ⭐⭐⭐⭐⭐ 夯 - 智能体工作流与任务协作
- [muratcankoylan/multi-agent-patterns](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/tree/main/skills/multi-agent-patterns) ⭐⭐⭐⭐⭐ 夯 - 智能体工作流与任务协作
- [obra/dispatching-parallel-agents](https://github.com/obra/superpowers/blob/main/skills/dispatching-parallel-agents/SKILL.md) ⭐⭐⭐⭐⭐ 夯 - 智能体工作流与任务协作
- [obra/subagent-driven-development](https://github.com/obra/superpowers/blob/main/skills/subagent-driven-development/SKILL.md) ⭐⭐⭐⭐⭐ 夯 - 智能体工作流与任务协作
- [obra/testing-skills-with-subagents](https://github.com/obra/superpowers/blob/main/skills/testing-skills-with-subagents/SKILL.md) ⭐⭐⭐⭐⭐ 夯 - 智能体工作流与任务协作
- [NeoLabHQ/prompt-engineering](https://github.com/NeoLabHQ/context-engineering-kit/tree/master/plugins/customaize-agent/skills/prompt-engineering) ⭐⭐⭐⭐⭐ 夯 - 智能体工作流与任务协作
- [muratcankoylan/context-degradation](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/tree/main/skills/context-degradation) ⭐⭐⭐⭐⭐ 夯 - 智能体与提示词工程
- [muratcankoylan/context-compression](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/tree/main/skills/context-compression) ⭐⭐⭐⭐⭐ 夯 - 智能体与提示词工程

### 大模型（39个）

- [NVIDIA/Model-Optimizer/launching-evals](https://github.com/NVIDIA/skills/tree/main/skills/Model-Optimizer/launching-evals) ⭐⭐⭐⭐⭐ 夯 - 大语言模型训练、推理或评估
- [NVIDIA/NeMo-Evaluator-Launcher/launching-evals](https://github.com/NVIDIA/skills/tree/main/skills/NeMo-Evaluator-Launcher/launching-evals) ⭐⭐⭐⭐⭐ 夯 - 大语言模型训练、推理或评估
- [NVIDIA/Megatron-Bridge/perf-moe-hardware-configs](https://github.com/NVIDIA/skills/tree/main/skills/Megatron-Bridge/perf-moe-hardware-configs) ⭐⭐⭐⭐⭐ 夯 - 大模型训练工程
- [NVIDIA/Megatron-Bridge/recipe-recommender](https://github.com/NVIDIA/skills/tree/main/skills/Megatron-Bridge/recipe-recommender) ⭐⭐⭐⭐⭐ 夯 - 大模型训练工程
- [NVIDIA/TensorRT-LLM/kernel-tileir-optimization](https://github.com/NVIDIA/skills/tree/main/skills/TensorRT-LLM/kernel-tileir-optimization) ⭐⭐⭐⭐⭐ 夯 - 大语言模型训练、推理或评估
- [NVIDIA/TensorRT-LLM/perf-host-analysis](https://github.com/NVIDIA/skills/tree/main/skills/TensorRT-LLM/perf-host-analysis) ⭐⭐⭐⭐⭐ 夯 - 大语言模型训练、推理或评估
- [NVIDIA/Model-Optimizer/evaluation](https://github.com/NVIDIA/skills/tree/main/skills/Model-Optimizer/evaluation) ⭐⭐⭐⭐⭐ 夯 - 大语言模型训练、推理或评估
- [NVIDIA/Model-Optimizer/monitor](https://github.com/NVIDIA/skills/tree/main/skills/Model-Optimizer/monitor) ⭐⭐⭐⭐⭐ 夯 - 大模型训练、推理与评估

### 数据检索（1个）

- [NVIDIA/rag/rag-blueprint](https://github.com/NVIDIA/skills/tree/main/skills/rag/rag-blueprint) ⭐⭐⭐⭐ 顶级 - 检索增强生成与知识问答

### 其他 / 暂未明确（4个）

- [NVIDIA/TileGym/improve-cutile-kernel-perf](https://github.com/NVIDIA/skills/tree/main/skills/TileGym/improve-cutile-kernel-perf) ⭐⭐⭐⭐ 顶级 - 综合型人工智能技能应用
- [NVIDIA/cuopt/cuopt-server-common](https://github.com/NVIDIA/skills/tree/main/skills/cuopt/cuopt-server-common) ⭐⭐⭐⭐ 顶级 - 综合型人工智能技能应用
- [NVIDIA/cuopt/cuopt-user-rules](https://github.com/NVIDIA/skills/tree/main/skills/cuopt/cuopt-user-rules) ⭐⭐⭐⭐ 顶级 - 综合型人工智能技能应用