// tslint:disable-next-line:interface-name
import LoginUserUseCase from '../../../usecase/user/login';
import SocketRegistryContainer from '../entity/sockets_registry';

// tslint:disable-next-line:interface-name
export default interface WebSocketsInterface {
  registerSocketEventsAndHandlers({
    socketRegistryContainers,
  }: {
    socketRegistryContainers: [SocketRegistryContainer];
  }): WebSocketsInterface;

  login({ loginUserUseCase }: { loginUserUseCase: LoginUserUseCase }): (...args: any) => any;

  serve({ host, port, starterFunc }: { host: string; port: number; starterFunc: (...args: any) => any }): void;
}
