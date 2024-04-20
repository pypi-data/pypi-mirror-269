// @generated
// Note: The protobuf definition is shared between the Rust and Swift parts.
// We are not using prost-build because providing protoc is a hassle on many platforms.
// See .github/workflows/autofix.yml for how to update the respective files,
// or file a PR and let CI handle it.

/// Packet with associated tunnel info (Windows pipe to mitmproxy)
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct PacketWithMeta {
    #[prost(bytes = "vec", tag = "1")]
    pub data: ::prost::alloc::vec::Vec<u8>,
    #[prost(message, optional, tag = "2")]
    pub tunnel_info: ::core::option::Option<TunnelInfo>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct TunnelInfo {
    #[prost(uint32, tag = "1")]
    pub pid: u32,
    #[prost(string, optional, tag = "2")]
    pub process_name: ::core::option::Option<::prost::alloc::string::String>,
}
/// Packet or intercept spec (Windows pipe to redirector)
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct FromProxy {
    #[prost(oneof = "from_proxy::Message", tags = "1, 2")]
    pub message: ::core::option::Option<from_proxy::Message>,
}
/// Nested message and enum types in `FromProxy`.
pub mod from_proxy {
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Message {
        #[prost(message, tag = "1")]
        Packet(super::Packet),
        #[prost(message, tag = "2")]
        InterceptConf(super::InterceptConf),
    }
}
/// Packet (macOS UDP Stream)
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Packet {
    #[prost(bytes = "vec", tag = "1")]
    pub data: ::prost::alloc::vec::Vec<u8>,
}
/// Intercept conf (macOS Control Stream)
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct InterceptConf {
    #[prost(uint32, repeated, tag = "1")]
    pub pids: ::prost::alloc::vec::Vec<u32>,
    #[prost(string, repeated, tag = "2")]
    pub process_names: ::prost::alloc::vec::Vec<::prost::alloc::string::String>,
    #[prost(bool, tag = "3")]
    pub invert: bool,
}
/// New flow (macOS TCP/UDP Stream)
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct NewFlow {
    #[prost(oneof = "new_flow::Message", tags = "1, 2")]
    pub message: ::core::option::Option<new_flow::Message>,
}
/// Nested message and enum types in `NewFlow`.
pub mod new_flow {
    #[allow(clippy::derive_partial_eq_without_eq)]
    #[derive(Clone, PartialEq, ::prost::Oneof)]
    pub enum Message {
        #[prost(message, tag = "1")]
        Tcp(super::TcpFlow),
        #[prost(message, tag = "2")]
        Udp(super::UdpFlow),
    }
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct TcpFlow {
    #[prost(message, optional, tag = "1")]
    pub remote_address: ::core::option::Option<Address>,
    #[prost(message, optional, tag = "2")]
    pub tunnel_info: ::core::option::Option<TunnelInfo>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct UdpFlow {
    #[prost(message, optional, tag = "1")]
    pub local_address: ::core::option::Option<Address>,
    #[prost(message, optional, tag = "3")]
    pub tunnel_info: ::core::option::Option<TunnelInfo>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct UdpPacket {
    #[prost(bytes = "vec", tag = "1")]
    pub data: ::prost::alloc::vec::Vec<u8>,
    #[prost(message, optional, tag = "2")]
    pub remote_address: ::core::option::Option<Address>,
}
#[allow(clippy::derive_partial_eq_without_eq)]
#[derive(Clone, PartialEq, ::prost::Message)]
pub struct Address {
    #[prost(string, tag = "1")]
    pub host: ::prost::alloc::string::String,
    #[prost(uint32, tag = "2")]
    pub port: u32,
}
// @@protoc_insertion_point(module)
