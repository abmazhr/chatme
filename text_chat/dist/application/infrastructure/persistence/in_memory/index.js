"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const failure_1 = __importDefault(require("../../../../domain/entity/failure"));
const success_1 = __importDefault(require("../../../../domain/entity/success"));
const types_1 = require("../../../../domain/types");
class InMemoryDatabase {
    constructor() {
        // tslint:disable-next-line:variable-name
        this._db = {};
    }
    fetchAccessToken({ username }) {
        const fetchStatus = this._db[username];
        return fetchStatus
            ? types_1.right(fetchStatus)
            : types_1.left(new failure_1.default({ error: `There is no access-token for user ${username}` }));
    }
    persistAccessToken({ username, accessToken, }) {
        try {
            this._db[username] = accessToken;
            return types_1.right(new success_1.default());
        }
        catch (e) {
            return types_1.left(new failure_1.default(e.toString()));
        }
    }
}
exports.default = InMemoryDatabase;
//# sourceMappingURL=index.js.map