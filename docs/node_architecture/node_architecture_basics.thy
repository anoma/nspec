theory node_architecture_basics
imports Main
        prelude
begin

type_synonym Identity = "nat \<times> nat"

type_synonym Name = "(string, nat) Either"

record 'MessageType MessagePacket =
  target :: "(string, nat) Either"
  mailbox :: "nat option"
  message :: 'MessageType

record 'MessageType EnvelopedMessage =
  sender :: "((string, nat) Either) option"
  packet :: "'MessageType MessagePacket"

fun target :: "'MessageType MessagePacket \<Rightarrow> Name" where
  "target (| MessagePacket.target = target', MessagePacket.mailbox = mailbox', MessagePacket.message = message' |) =
    target'"

fun mailbox :: "'MessageType MessagePacket \<Rightarrow> nat option" where
  "mailbox (| MessagePacket.target = target', MessagePacket.mailbox = mailbox', MessagePacket.message = message' |) =
    mailbox'"

fun message :: "'MessageType MessagePacket \<Rightarrow> 'MessageType" where
  "message (| MessagePacket.target = target', MessagePacket.mailbox = mailbox', MessagePacket.message = message' |) =
    message'"

fun sender :: "'MessageType EnvelopedMessage \<Rightarrow> Name option" where
  "sender (| EnvelopedMessage.sender = sender', EnvelopedMessage.packet = packet' |) = sender'"

fun packet :: "'MessageType EnvelopedMessage \<Rightarrow> 'MessageType MessagePacket" where
  "packet (| EnvelopedMessage.sender = sender', EnvelopedMessage.packet = packet' |) = packet'"

fun getMessageType :: "'M EnvelopedMessage \<Rightarrow> 'M" where
  "getMessageType (| EnvelopedMessage.sender = gen_0, EnvelopedMessage.packet = v |) =
    (MessagePacket.message v)"

fun getMessageSender :: "'M EnvelopedMessage \<Rightarrow> Name option" where
  "getMessageSender (| EnvelopedMessage.sender = s, EnvelopedMessage.packet = gen_1 |) = s"

fun getMessageTarget :: "'M EnvelopedMessage \<Rightarrow> Name" where
  "getMessageTarget (| EnvelopedMessage.sender = gen_0, EnvelopedMessage.packet = v |) =
    (MessagePacket.target v)"

record ('MessageType, 'MailboxStateType) Mailbox =
  messages :: "('MessageType EnvelopedMessage) list"
  mailboxState :: "'MailboxStateType option"

record 'HandleType Timer =
  time :: nat
  handle :: 'HandleType

datatype ('MessageType, 'HandleType) Trigger
  = MessageArrived "'MessageType EnvelopedMessage" |
    Elapsed "('HandleType Timer) list"

fun messages :: "('MessageType, 'MailboxStateType) Mailbox \<Rightarrow> ('MessageType EnvelopedMessage) list" where
  "messages (| Mailbox.messages = messages', Mailbox.mailboxState = mailboxState' |) = messages'"

fun mailboxState :: "('MessageType, 'MailboxStateType) Mailbox \<Rightarrow> 'MailboxStateType option" where
  "mailboxState (| Mailbox.messages = messages', Mailbox.mailboxState = mailboxState' |) =
    mailboxState'"

fun time :: "'HandleType Timer \<Rightarrow> nat" where
  "time (| Timer.time = time', Timer.handle = handle' |) = time'"

fun handle :: "'HandleType Timer \<Rightarrow> 'HandleType" where
  "handle (| Timer.time = time', Timer.handle = handle' |) = handle'"

fun getMessageFromTrigger :: "('M, 'H) Trigger \<Rightarrow> 'M option" where
  "getMessageFromTrigger v_0 =
    (case (v_0) of
       (MessageArrived v) \<Rightarrow>
         (case (EnvelopedMessage.packet v) of
            (v') \<Rightarrow> Some (MessagePacket.message v')) |
       v'0 \<Rightarrow> None)"

fun getMessageSenderFromTrigger :: "('M, 'H) Trigger \<Rightarrow> Name option" where
  "getMessageSenderFromTrigger (MessageArrived e) = (node_architecture_basics.sender e)" |
  "getMessageSenderFromTrigger v = None"

fun getMessageTargetFromTrigger :: "('M, 'H) Trigger \<Rightarrow> Name option" where
  "getMessageTargetFromTrigger v_0 =
    (case (v_0) of
       (MessageArrived v) \<Rightarrow>
         (case (EnvelopedMessage.packet v) of
            (v') \<Rightarrow> Some (MessagePacket.target v')) |
       v'0 \<Rightarrow> None)"

record ('MessageType, 'HandleType) TimestampedTrigger =
  time :: nat
  trigger :: "('MessageType, 'HandleType) Trigger"

(*
fun time :: "('MessageType, 'HandleType) TimestampedTrigger \<Rightarrow> nat" where
  "time (| TimestampedTrigger.time = time', TimestampedTrigger.trigger = trigger' |) = time'"
*)

fun trigger :: "('MessageType, 'HandleType) TimestampedTrigger \<Rightarrow> ('MessageType, 'HandleType) Trigger" where
  "trigger (| TimestampedTrigger.time = time', TimestampedTrigger.trigger = trigger' |) = trigger'"

fun getMessageFromTimestampedTrigger :: "('M, 'H) TimestampedTrigger \<Rightarrow> 'M option" where
  "getMessageFromTimestampedTrigger tr =
    (getMessageFromTrigger (node_architecture_basics.trigger tr))"

fun getMessageSenderFromTimestampedTrigger :: "('M, 'H) TimestampedTrigger \<Rightarrow> Name option" where
  "getMessageSenderFromTimestampedTrigger tr =
    (getMessageSenderFromTrigger (node_architecture_basics.trigger tr))"

fun getMessageTargetFromTimestampedTrigger :: "('M, 'H) TimestampedTrigger \<Rightarrow> Name option" where
  "getMessageTargetFromTimestampedTrigger tr =
    (getMessageTargetFromTrigger (node_architecture_basics.trigger tr))"

end
