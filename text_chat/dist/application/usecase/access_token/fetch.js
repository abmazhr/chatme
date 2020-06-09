"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class FetchAccessTokenUseCase {
    constructor(persistence) {
        this._persistence = persistence;
    }
    execute({ username }) {
        return Promise.resolve(this._persistence.fetchAccessToken({ username }));
    }
}
exports.default = FetchAccessTokenUseCase;
//# sourceMappingURL=fetch.js.map