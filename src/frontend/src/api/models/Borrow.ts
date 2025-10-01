/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type Borrow = {
    /**
     * The copy ID
     */
    copyId: string;
    /**
     * Borrow creation timestamp
     */
    readonly createdAt?: string;
    /**
     * The borrow ID
     */
    readonly id?: string;
    /**
     * The patron ID
     */
    patronId: string;
    /**
     * Borrow status: BORROWING, RETURNED, or LOST
     */
    status: string;
    /**
     * Last status update timestamp
     */
    readonly statusLastUpdatedAt?: string;
};

