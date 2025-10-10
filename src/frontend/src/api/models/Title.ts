/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type Title = {
    /**
     * The title ID
     */
    readonly id?: string;
    /**
     * Title name
     */
    name: string;
    /**
     * Edition number
     */
    edition: number;
    /**
     * Newline-separated list of authors
     */
    authors: string;
    /**
     * Year of publication
     */
    yearOfPublication: number;
    /**
     * Newline-separated list of tags
     */
    tags: string;
    /**
     * Total number of copies
     */
    readonly totalCopies?: number;
    /**
     * Number of available copies
     */
    readonly availableCopies?: number;
    /**
     * Number of borrowed copies
     */
    readonly borrowedCopies?: number;
    /**
     * Number of lost copies
     */
    readonly lostCopies?: number;
};

