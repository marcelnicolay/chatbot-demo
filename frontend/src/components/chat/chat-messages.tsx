import { cn } from "@/lib/utils"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Message } from "./interface"


function MessageItem({children, role}: {children: string, role:string}) {

  return (
    <>
      <div className="flex flex-row text-xs">
        {role === "assistant" ? (
          <Avatar className="hidden h-9 w-9 sm:flex">
          <AvatarImage src="/avatar.png" alt="Avatar" />
          <AvatarFallback>AVA</AvatarFallback>
        </Avatar>
        ): null}
        
        <div className={cn(
            role === "user"
              ? "ml-auto rounded-tl-xl p-2 rounded-br-xl rounded-bl-xl border bg-primary text-primary-foreground"
              : "ml-2 bg-muted rounded-tr-xl p-2 rounded-br-xl rounded-bl-xl border bg-background text-foreground"
          )}
        >
          {children}
        </div>
      </div>
    </>
  )
}

export function ChatMessages(props: {messages: Message[]}) {
    return (
      <>
          {props.messages.map((message, index) => (
            <MessageItem key={index} role={message.role}>{message.content}</MessageItem>             
          ))}
        </>
    )
}