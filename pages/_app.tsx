import type { AppProps } from 'next/app'
import { Analytics } from '@vercel/analytics/react'

import Layout, { getLayout } from '../components/Layout'

import '@vercel/examples-ui/globals.css'

function App({ Component, pageProps }: AppProps) {

  return (
    <Layout
      title="ask-my-book-chatbot"
      path="ask-my-book-chatbot"
      description="ai-chatbot-that-understands-your-book"
      
    >
      <Component {...pageProps} />
      <Analytics />
    </Layout>
  )
}

export default App
