/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type Copy = {
    /**
     * The copy ID
     */
    readonly id?: string;
    /**
     * The title ID this copy belongs to
     */
    titleId: string;
    /**
     * Copy code/identifier
     */
    code: string;
    /**
     * Current status: AVAILABLE, BORROWED, or LOST
     */
    readonly status?: string;
};

