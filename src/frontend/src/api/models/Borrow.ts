/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type Borrow = {
    /**
     * The borrow ID
     */
    readonly id?: string;
    /**
     * The patron ID
     */
    patronId: string;
    /**
     * The copy ID
     */
    copyId: string;
    /**
     * Borrow status: BORROWING, RETURNED, or LOST
     */
    status: string;
    /**
     * Borrow creation timestamp
     */
    readonly createdAt?: string;
    /**
     * Last status update timestamp
     */
    readonly statusLastUpdatedAt?: string;
};

