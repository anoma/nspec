pub struct MessageContentV0 {
    // source
    pub src: ExternalIdentity,
    // destination
    pub dst: ExternalIdentity,
    // protocol + version
    pub protocol: Protocol,
    // expiry: time after which the message should be deleted if undelivered
    pub expiry: u32,
    // serialized message body
    pub body: Vec<u8>,
}
pub struct MessageV0 {
    pub content: MessageContentV0,
    // signature over content by src
    pub sig: Option<Sig>,
}
pub enum Message {
    V0(MessageV0)
}
