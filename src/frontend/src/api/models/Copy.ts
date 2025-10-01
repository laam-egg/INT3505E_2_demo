/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type Copy = {
    /**
     * Copy code/identifier
     */
    code: string;
    /**
     * The copy ID
     */
    readonly id?: string;
    /**
     * Current status: AVAILABLE, BORROWED, or LOST
     */
    readonly status?: string;
    /**
     * The title ID this copy belongs to
     */
    titleId: string;
};

