import express from 'express';
import { createServer, Server } from 'http';
import socketIO from 'socket.io';
import logger from '../../../../../domain/common/logger';
import LoginUserUseCase from '../../../../usecase/user/login';
import WebSocketsInterface from '../index';

export default class ExpressWebSockets implements WebSocketsInterface {
  private readonly _restApi: express.Application;
  private readonly _socketsApi: socketIO.Server;
  private readonly _httpServer: Server;

  constructor({ loginUserUseCase }: { loginUserUseCase: LoginUserUseCase }) {
    this._restApi = express();
    this._httpServer = createServer(this._restApi);
    this._socketsApi = socketIO(this._httpServer);
    this.login({ loginUserUseCase });
  }

  public serve({ port, starterFunc }: { port: number; starterFunc: (...args: any) => any }): void {
    this._httpServer.listen(port, starterFunc);
  }

  public login({ loginUserUseCase }: { loginUserUseCase: LoginUserUseCase }): any {
    this._socketsApi.addListener('connection', async (socket: socketIO.Socket) => {
        const username: string = socket.request.headers.username;
        const password: string = socket.request.headers.password;

        if (username && password) {
          const loginStatus = await loginUserUseCase.execute({ username, password });
          switch (loginStatus._tag) {
            case 'Left': {
              socket.error(loginStatus.left.error);
              socket.disconnect(true);
              break;
            }
            case 'Right': {
              const msg = `Client ${socket.id} has been logged in and connected.`;
              logger.info(msg);
              this.broadcastMessageToAll({
                broadCaster: this._socketsApi,
                message: msg,
                event: process.env.NOTIFICATIONS_EVENT_NAME || 'notifications',
              });
              socket.join(process.env.CHAT_ROOM_NAME || 'chat');
              socket.on(process.env.SEND_RECEIVE_MESSAGE_EVENT_NAME || 'message', this.receiveMessage({
                socket,
              }));
              socket.on('disconnect', this.logout({ socket }));
              break;
            }
          }
        } else {
          socket.error('You should provide [username, password] in your headers to login.');
          socket.disconnect(true);
        }
      },
    );
  }

  public logout({ socket }: { socket: socketIO.Socket }): (...args: any) => any {
    const broadCaster = this._socketsApi;
    const broadcastMessageToAllFunc = this.broadcastMessageToAll;
    const event = process.env.NOTIFICATIONS_EVENT_NAME || 'notifications';
    return function() {
      const msg = `Client ${socket.id} has been logged out.`;
      logger.info(msg);
      broadcastMessageToAllFunc({
        event,
        message: msg,
        broadCaster,
      });
    };
  }

  public receiveMessage({ socket }: { socket: socketIO.Socket }): (...args: any) => any {
    const room = process.env.CHAT_ROOM_NAME || 'chat';
    const event = process.env.SEND_RECEIVE_MESSAGE_EVENT_NAME || 'message';
    const broadCaster = this._socketsApi;
    const broadcastMessageToRoomFunc = this.broadcastMessageToRoom;
    return function(message: string) {
      logger.info(`Client: ${socket.id} has received message: ${message}`);
      broadcastMessageToRoomFunc({
        room,
        broadCaster,
        message,
        event,
      });
    };
  }

  public broadcastMessageToRoom({ broadCaster, room, message, event }: {
    broadCaster: socketIO.Server
    room: string
    message: string
    event: string
  }): any {
    broadCaster.to(room).emit(event, message);
  }

  public broadcastMessageToAll({ broadCaster, message, event }: {
    broadCaster: socketIO.Server
    message: string
    event: string
  }): any {
    broadCaster.emit(event, message);
  }
}
