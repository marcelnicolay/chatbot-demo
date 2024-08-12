"use client"

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardFooter,
  CardTitle,
} from "@/components/ui/card"
import React from "react"
import { cn } from "@/lib/utils"
import { Send } from "lucide-react"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"

export function ChatWidget() {

  const [input, setInput] = React.useState("")
  const inputLength = input.trim().length  

  const [messages, setMessages] = React.useState([{
    role: "assistant",
    content: "Hi, how can I help you today?",
  }, {
    role: "user",
    content: "sure",
  }])

  return (
      <Card className="flex flex-col mx-auto w-[320px] h-[480px]">
        <CardHeader>
          <CardTitle className="text-2xl">Hey I'm Ava</CardTitle>
          <CardDescription>
            Ask me anything about our products
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4 text-sm overflow-y-auto h-[260px]">
            {messages.map((message, index) => (
              <div key={index} className="flex flex-row">
                {message.role === "assistant" ? (
                  <Avatar className="hidden h-9 w-9 sm:flex">
                  <AvatarImage src="/avatar.png" alt="Avatar" />
                  <AvatarFallback>AVA</AvatarFallback>
                </Avatar>
                ): null}
                
                <div className={cn(
                    message.role === "user"
                      ? "ml-auto rounded-tl-xl p-2 rounded-br-xl rounded-bl-xl border bg-primary text-primary-foreground"
                      : "ml-2 bg-muted rounded-tr-xl p-2 rounded-br-xl rounded-bl-xl border bg-background text-foreground"
                  )}
                >
                  {message.content}
                </div>
              </div>
            ))}
         </div>        
        </CardContent>
        <CardFooter>
          <div className="flex w-full items-end border-t-2 rounded-t-lg bg-background">
            <form className="flex flex-row overflow-hidden w-full" onSubmit={(event) => {
              event.preventDefault()
              if (inputLength === 0) return
              setMessages([
                ...messages,
                {
                  role: "user",
                  content: input,
                },
              ])
              setInput("")
            }}>
              <Input
                id="message"
                placeholder="Type your message here..."
                className="min-h-12 resize-none border-0 p-3 shadow-none focus-visible:ring-0 text-foreground"
                value={input}
                onChange={(event) => setInput(event.target.value)}
              />
              <div className="relative flex-col gap-2 px-8">
                <Button type="submit" size="icon" className="absolute bottom-0 right-0 h-8 w-8" disabled={inputLength === 0}>
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