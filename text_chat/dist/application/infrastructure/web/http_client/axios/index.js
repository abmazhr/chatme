"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const axios_1 = __importDefault(require("axios"));
const failure_1 = __importDefault(require("../../../../../domain/entity/failure"));
const types_1 = require("../../../../../domain/types");
const http_response_1 = __importDefault(require("../../entity/http_response"));
class AxiosHttpClient {
    get({ endpoint, config }) {
        return axios_1.default
            .get(endpoint, config)
            .then((response) => types_1.right(new http_response_1.default({ data: response.data, statusCode: response.status })))
            .catch((error) => types_1.left(new failure_1.default({ error })));
    }
    post({ endpoint, data, config, }) {
        return axios_1.default
            .post(endpoint, data, config)
            .then((response) => types_1.right(new http_response_1.default({ data: response.data, statusCode: response.status })))
            .catch((error) => types_1.left(new failure_1.default({ error })));
    }
}
exports.default = AxiosHttpClient;
//# sourceMappingURL=index.js.map