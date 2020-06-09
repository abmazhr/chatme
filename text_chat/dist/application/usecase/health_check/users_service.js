"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const success_1 = __importDefault(require("../../../domain/entity/success"));
const types_1 = require("../../../domain/types");
class UsersServiceHealthCheckUseCase {
    constructor({ usersServiceHealthCheckEndpoint, httpClient, }) {
        this._usersServiceHealthCheckEndpoint = usersServiceHealthCheckEndpoint;
        this._httpClient = httpClient;
    }
    execute() {
        return this._httpClient.get({ endpoint: this._usersServiceHealthCheckEndpoint }).then((response) => {
            switch (response._tag) {
                case 'Left':
                    return response;
                case 'Right':
                    return types_1.right(new success_1.default());
            }
        });
    }
}
exports.default = UsersServiceHealthCheckUseCase;
//# sourceMappingURL=users_service.js.map