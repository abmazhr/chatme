"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const os = __importStar(require("os"));
const sockets_registry_1 = __importDefault(require("./application/infrastructure/web/entity/sockets_registry"));
const axios_1 = __importDefault(require("./application/infrastructure/web/http_client/axios"));
const express_sockets_1 = __importDefault(require("./application/infrastructure/web/sockets/express_sockets"));
const users_service_1 = __importDefault(require("./application/usecase/health_check/users_service"));
const login_1 = __importDefault(require("./application/usecase/user/login"));
const logger_1 = __importDefault(require("./domain/common/logger"));
const httpClient = new axios_1.default();
const port = parseInt(process.env.PORT);
const usersServiceHealthCheckEndpoint = process.env.USERS_SERVICE_HEALTH_CHECK_ENDPOINT;
const usersServiceLoginEndpoint = process.env.USERS_SERVICE_LOGIN_ENDPOINT;
new express_sockets_1.default({
    socketRegistryContainers: [
        new sockets_registry_1.default({
            eventHandler: express_sockets_1.default.login({
                loginUserUseCase: new login_1.default({
                    httpClient,
                    usersServiceHealthCheckUseCase: new users_service_1.default({
                        httpClient,
                        usersServiceHealthCheckEndpoint,
                    }),
                    usersServiceLoginEndpoint,
                }),
            }),
            eventName: 'connection',
        }),
    ],
}).serve({
    port,
    starterFunc: () => logger_1.default.info(`up and running in ${process.env.NODE_ENV || 'development'} @: ${os.hostname()} on port: ${port}}`),
});
//# sourceMappingURL=index.js.map