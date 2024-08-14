pub struct RelayMessageContentV0 {
    // source
    pub src: ExternalIdentity,
    // destination
    pub dst: ExternalIdentity,
    // expiry: time after which the message should be deleted if undelivered
    pub expiry: u32,
    // encrypted message
    pub msg: Vec<u8>,
    // MAC over msg
    pub mac: Vec<u8>,
}
pub struct RelayMessageV0 {
    pub content: RelayMessageContentV0,
    // signature over content by src
    pub sig: Sig,
}
pub enum RelayMessage {
    V0(RelayMessageV0)
}
