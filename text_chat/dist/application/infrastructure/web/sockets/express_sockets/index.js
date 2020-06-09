"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const http_1 = require("http");
const socket_io_1 = __importDefault(require("socket.io"));
class ExpressWebSockets {
    constructor({ socketRegistryContainers }) {
        this._restApi = express_1.default();
        this._httpServer = http_1.createServer(this._restApi);
        this._socketsApi = socket_io_1.default(this._httpServer);
        this.registerSocketEventsAndHandlers({ socketRegistryContainers });
    }
    static login({ loginUserUseCase }) {
        return (socket) => __awaiter(this, void 0, void 0, function* () {
            const username = socket.request.headers.username;
            const password = socket.request.headers.password;
            if (username && password) {
                const loginStatus = yield loginUserUseCase.execute({ username, password });
                switch (loginStatus._tag) {
                    case 'Left': {
                        socket.error(loginStatus.left.error);
                        socket.disconnect(true);
                    }
                }
            }
            else {
                socket.error('You should provide [username, password] in your headers to login.');
                socket.disconnect(true);
            }
        });
    }
    registerSocketEventsAndHandlers({ socketRegistryContainers, }) {
        socketRegistryContainers.forEach((container) => {
            this._socketsApi.addListener(container.eventName, container.eventHandler);
        });
        return this;
    }
    serve({ port, starterFunc }) {
        this._httpServer.listen(port, starterFunc);
    }
    // Maybe there is a better way for this static thing later? ;)
    login({ loginUserUseCase }) {
        return ExpressWebSockets.login({ loginUserUseCase });
    }
}
exports.default = ExpressWebSockets;
//# sourceMappingURL=index.js.map