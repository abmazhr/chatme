import * as express from 'express';
import { createServer, Server } from 'http';
import * as socketIO from 'socket.io';
import LoginUserUseCase from '../../../../usecase/user/login';
import SocketRegistryContainer from '../../entity/sockets_registry';
import WebSocketsInterface from '../index';

export default class ExpressWebSockets implements WebSocketsInterface {
  // @ts-ignore
  public static login({ loginUserUseCase }: { loginUserUseCase: LoginUserUseCase }): (...args: any) => any {
    return async (socket: socketIO.Socket) => {
      const username: string = socket.request.headers.username;
      const password: string = socket.request.headers.password;

      if (username && password) {
        const loginStatus = await loginUserUseCase.execute({ username, password });
        switch (loginStatus._tag) {
          case 'Left': {
            socket.error(loginStatus.left.error);
            socket.disconnect(true);
          }
        }
      } else {
        socket.error('You should provide [username, password] in your headers to login.');
        socket.disconnect(true);
      }
    };
  }

  // tslint:disable-next-line:variable-name
  private readonly _restApi: express.Application;
  // tslint:disable-next-line:variable-name
  private readonly _socketsApi: socketIO.Server;
  // tslint:disable-next-line:variable-name
  private readonly _httpServer: Server;

  constructor({ socketRegistryContainers }: { socketRegistryContainers: [SocketRegistryContainer] }) {
    this._restApi = express();
    this._httpServer = createServer(this._restApi);
    this._socketsApi = socketIO(this._httpServer);

    this.registerSocketEventsAndHandlers({ socketRegistryContainers });
  }

  public registerSocketEventsAndHandlers({
    socketRegistryContainers,
  }: {
    socketRegistryContainers: [SocketRegistryContainer];
  }): ExpressWebSockets {
    socketRegistryContainers.forEach(container => {
      this._socketsApi.addListener(container.eventName, container.eventHandler);
    });
    return this;
  }

  public serve({ port, starterFunc }: { port: number; starterFunc: (...args: any) => any }): void {
    this._httpServer.listen(port, starterFunc);
  }

  // Maybe there is a better way for this static thing later? ;)
  public login({ loginUserUseCase }: { loginUserUseCase: LoginUserUseCase }): (...args: any) => any {
    return ExpressWebSockets.login({ loginUserUseCase });
  }
}
