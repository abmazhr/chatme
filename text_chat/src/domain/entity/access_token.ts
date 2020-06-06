// tslint:disable-next-line:interface-name
export default class AccessToken {
  public readonly token: string;

  constructor({ token }: { token: string }) {
    this.token = token;
  }
}
