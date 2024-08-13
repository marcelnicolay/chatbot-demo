import { cn } from "@/lib/utils"
import { Label } from "@/components/ui/label"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Message } from "./interface"


export function ChatMessages(props: {messages: Message[]}) {
    return (
        <>
            {props.messages.map((message, index) => (
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
         </>
    )
}