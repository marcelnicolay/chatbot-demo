"use client"

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardFooter,
  CardTitle,
} from "@/components/ui/card"
import React, { useState, useEffect } from "react"
import { Send, Loader2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { ChatMessages } from "./chat-messages"
import { Message, Thread } from "./interface"
import { ChatApi } from "./chat-api"


export function ChatWidget() {
  
  const [isLoading, setIsLoading] = useState(false);
  const [activeThread, setActiveThread] = useState<Thread>();
  const [messages, setMessages] = useState<Message[]>([
    { 
      role: "assistant", 
      content: "Hi there! How can I help you today?" 
    } as Message
  ]);
  
  useEffect(() => {

    setIsLoading(true);
    ChatApi.createThread().then((thread) => {
      setActiveThread(thread)
      setIsLoading(false)
    })

  }, [])

  const [input, setInput] = React.useState("")
  const inputLength = input.trim().length  

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault()
    if (inputLength === 0) return
    if (activeThread === undefined) return

    const newMessage = { role: "user", content: input } as Message
    setMessages([...messages, newMessage]);
    console.log(messages)
    
    // call the chat api
    ChatApi.callChatApi({
      thread: activeThread,
      messages: [...messages, newMessage],
      headers: {},
      onResponse: (message) => {
        setMessages([...messages, newMessage, message]);
      },
      onError: (error) => {
        console.error(error);
      }
    });

    setInput("")
  }

  return (
      <Card className="flex flex-col mx-auto w-[320px] h-[480px]">
        <CardHeader>
          <CardTitle className="text-2xl">Hey I'm Ava</CardTitle>
          <CardDescription>
            Ask me anything about our products
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4 text-sm overflow-y-auto h-[260px] pr-2">
            {isLoading ? (
                  <div className="flex p-4 justify-center items-center">
                    <Loader2 className="h-4 w-4 animate-spin" />
                  </div>
                ) : (
              <ChatMessages messages={messages} /> 
            )}
          </div>
        </CardContent>
        <CardFooter>
          <div className="flex w-full items-end border-t-2 rounded-t-lg bg-background">
            <form className="flex flex-row overflow-hidden w-full" onSubmit={handleSubmit}>
              <Input
                id="message"
                placeholder="Type your message here..."
                className="min-h-12 resize-none border-0 p-3 shadow-none focus-visible:ring-0 text-foreground"
                value={input}
                onChange={(event) => setInput(event.target.value)}
              />
              <div className="relative flex-col gap-2 px-8">
                <Button type="submit" size="icon" className="absolute bottom-0 right-0 h-8 w-8" disabled={inputLength === 0 || isLoading}>
                  <Send className="h-4 w-4" />
                  <span className="sr-only">Send</span>
                </Button>
              </div>
            </form>
          </div>
        </CardFooter>
    </Card>
  )
}