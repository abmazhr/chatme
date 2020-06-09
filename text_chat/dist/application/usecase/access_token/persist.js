"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class PersistAccessTokenUseCase {
    constructor(persistence) {
        this._persistence = persistence;
    }
    execute({ username, accessToken, }) {
        return Promise.resolve(this._persistence.persistAccessToken({ username, accessToken }));
    }
}
exports.default = PersistAccessTokenUseCase;
//# sourceMappingURL=persist.js.map