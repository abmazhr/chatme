// tslint:disable-next-line:no-submodule-imports
import { Option } from 'fp-ts/lib/Option';
// tslint:disable-next-line:no-submodule-imports
export { some, none } from 'fp-ts/lib/Option';
// tslint:disable-next-line:no-submodule-imports
export { Either, left, right } from 'fp-ts/lib/Either';
export type Maybe<T> = Option<T>;
