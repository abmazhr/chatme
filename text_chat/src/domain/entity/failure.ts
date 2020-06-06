// tslint:disable-next-line:interface-name
export default class Failure {
  public readonly error: string;

  constructor({ error }: { error: string }) {
    this.error = error;
  }
}
