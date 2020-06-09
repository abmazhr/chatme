"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const types_1 = require("../../../domain/types");
class LoginUserUseCase {
    constructor({ usersServiceHealthCheckUseCase, httpClient, usersServiceLoginEndpoint, }) {
        this._usersServiceUseCase = usersServiceHealthCheckUseCase;
        this._httpClient = httpClient;
        this._usersServiceLoginEndpoint = usersServiceLoginEndpoint;
    }
    execute({ username, password, }) {
        return Promise.resolve(this._usersServiceUseCase.execute().then((healthCheckResponse) => {
            switch (healthCheckResponse._tag) {
                case 'Left':
                    return healthCheckResponse;
                case 'Right':
                    return this._httpClient
                        .post({ endpoint: this._usersServiceLoginEndpoint, data: { username, password } })
                        .then((LoginResponse) => {
                        switch (LoginResponse._tag) {
                            case 'Left':
                                return LoginResponse;
                            case 'Right':
                                return types_1.right(LoginResponse.right.data);
                        }
                    });
            }
        }));
    }
}
exports.default = LoginUserUseCase;
//# sourceMappingURL=login.js.map