declare function _default<K, V>(as?: (id: number) => K): NextResolver<K, V>;
export default _default;
export type Resolve<V_1> = (value?: V_1 | null) => void;
export type Reject = (error?: any | null) => void;
export type Resolvers<V_1> = {
    promise: Promise<V_1>;
    resolve: Resolve<V_1>;
    reject: Reject;
};
export type Next<K_1, V_1> = () => [K_1, Promise<V_1>];
export type Resolver<K_1, V_1> = (uid: K_1, value?: V_1 | null, error?: any | null) => any;
export type NextResolver<K_1, V_1> = [Next<K_1, V_1>, Resolver<K_1, V_1>];
