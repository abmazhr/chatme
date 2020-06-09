export default class SocketRegistryContainer {
  public readonly eventName: string;
  public readonly eventHandler: ({ ...args }: { [p: string]: any }) => any;
  public readonly config?: any;

  constructor({
    eventName,
    eventHandler,
    config,
  }: {
    eventName: string;
    eventHandler: ({ ...args }: { [p: string]: any }) => any;
    config?: any;
  }) {
    this.eventName = eventName;
    this.eventHandler = eventHandler;
    this.config = config;
  }
}
