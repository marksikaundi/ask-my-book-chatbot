# Ask My Book 

### Build your own AI Chatbot trained on your own data

[![Steamship](https://raw.githubusercontent.com/steamship-core/python-client/main/badge.svg)](https://www.steamship.com/build/langchain-on-vercel?utm_source=github&utm_medium=badge&utm_campaign=github_repo&utm_id=github_vercel_repo_ai_chatgpt)

This example shows how to implement a persistent chat bot using Next.js, API Routes, [OpenAI](https://beta.openai.com/docs/api-reference/completions/create), and [Steamship](https://www.steamship.com).

![Screen Shot](https://steamship.com/data/templates/langchain-on-vercel/chatbot-card.png)

### Components

- Next.js
- OpenAI API (REST endpoint)
- API Routes (Edge runtime)
- Steamship API (AI orchestration stack)

## How to Use

### Run create-next-app

Execute [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app) with [npm](https://docs.npmjs.com/cli/init) or [Yarn](https://yarnpkg.com/lang/en/docs/cli/create/) to bootstrap the example:

```bash
npx create-next-app --example https://github.com/steamship-core/vercel-examples/tree/main/ask-my-book-chatbot
# or
yarn create next-app --example https://github.com/steamship-core/vercel-examples/tree/main/ask-my-book-chatbot
```

### Deploy your Steamship Stack

Steamship is an AI orchestration stack that auto-manages prompts, image generation, embeddings, vector search, and more.
Think of it as a host for Vercel-style API functions, but with a managed, stateful, AI stack built-in.

Deploy your Steamship stack from this project's root folder with:

```bash
cd _api
pip install -r requirements.txt
ship deploy
```

### Add your books

```commandline
cd _api
python upload/upload_local.py
# or 
python upload/upload_remote.py
```

### Set your environment variables

Rename [`.env.example`](.env.example) to `.env.local`:

```bash
cp .env.example .env.local
```

Then update `NEXT_PUBLIC_BASE_URL` with the base invocation url of package instance. You can get this using: 

```python
package_instance = client.use(
        PACKAGE_HANDLE, config={"index_name": INDEX_NAME}, version="0.2.0"
    )
print("BASE_URL:", package_instance.invocation_url)
```

### Run your web app

Run your Next.js stack in development mode:

```bash
npm install
npm run dev
# or
yarn
yarn dev
```

The app should be up and running at http://localhost:3000.

### Deploy your web app

You can deploy your web app with [Vercel](https://vercel.com/new?utm_source=github&utm_medium=readme&utm_campaign=steamship-ai-ask-my-book) ([Documentation](https://nextjs.org/docs/deployment)) by clicking [here](https://vercel.com/new/clone?s=https%3A%2F%2Fgithub.com%2Fsteamship-core%2Fvercel-examples%2Ftree%2Fmain%2Fask-my-book-chatbot&showOptionalTeamCreation=false&teamCreateStatus=hidden).

Please don't forget to add your [environment variables](https://vercel.com/docs/concepts/projects/environment-variables) in vercel.


