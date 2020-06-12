import LoginUserUseCase from '../../../usecase/user/login';

export default interface WebSocketsInterface {
  login({ loginUserUseCase }: {
    loginUserUseCase: LoginUserUseCase
  }): any

  logout({ socket }: { socket: any }): (...args: any) => any

  broadcastMessageToRoom({ broadCaster, room, message, event }: {
    broadCaster: any
    room: string
    message: string
    event: string
  }): any

  broadcastMessageToAll({ broadCaster, message, event }: {
    broadCaster: any
    message: string
    event: string
  }): any

  receiveMessage({ socket }: { socket: any }): (...args: any) => any

  serve({ host, port, starterFunc }: { host: string; port: number; starterFunc: (...args: any) => any }): void
}
