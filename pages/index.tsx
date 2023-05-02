import { Layout, Text, Page } from '@vercel/examples-ui'
import { Chat } from '../components/Chat'
import { useRouter } from 'next/router'
import Documents from "../components/Documents";
import { useState } from "react";

function Home() {
  const {query, isReady} = useRouter()


  const makeBaseUrl = (userHandle?: string, instanceHandle?: string, isStaging?: boolean) => {
    if (userHandle && instanceHandle){
      if (isStaging){
        return `https://${userHandle}.apps.staging.steamship.com/${instanceHandle}/${instanceHandle}`
    } else {
      return `https://${userHandle}.steamship.run/${instanceHandle}/${instanceHandle}`
    }
    } else {
      return null
    }
  }

  let {userHandle, instanceHandle, isStaging} = query
  const baseUrl = makeBaseUrl(userHandle as string, instanceHandle as string, isStaging === 'true') || process.env.NEXT_PUBLIC_BASE_URL as string;
  console.log("baseUrl", baseUrl)
  const errorMessage = (
        <div className="rounded-md bg-red-50 p-4">
            <div className="flex">
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <p>Front-end not connected.</p>
                <br/>
                <p>If this issue persists, please ping us on <a href="https://steamship.com/discord" className="font-semibold text-gray-900 underline dark:text-white decoration-sky-500">Discord</a>. We&apos;re happy to help. </p>
              </div>
            </div>
          </div>
          )

  return (
    <Page className="flex flex-col gap-12 ">
      <section className="flex flex-col gap-6 " >
        <Text variant="h1">Chat with your documents 🧠</Text>
        {isReady ? <Documents baseUrl={baseUrl}/>: <div/>}
      </section>

      <section className="flex flex-col gap-3">
        <div className="lg">
            { typeof baseUrl == "undefined" && errorMessage}
             <Chat baseUrl={baseUrl}/>
        </div>
      </section>
    </Page>
  )
}

Home.Layout = Layout

export default Home
