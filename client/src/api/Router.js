var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import axios from '../../node_modules/axios/index';
// Base URL of the API
const API_BASE_URL = 'http://194.61.53.28:8000/';
// const TOKEN =
//   'query_id=AAGOkjdJAAAAAI6SN0lDtNz9&user=%7B%22id%22%3A1228378766%2C%22first_name%22%3A%22%5B%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%7C%E2%80%A2%5D%22%2C%22last_name%22%3A%22%22%2C%22username%22%3A%22thinkfull%22%2C%22language_code%22%3A%22uk%22%2C%22is_premium%22%3Atrue%2C%22allows_write_to_pm%22%3Atrue%2C%22photo_url%22%3A%22https%3A%5C%2F%5C%2Ft.me%5C%2Fi%5C%2Fuserpic%5C%2F320%5C%2FO7kJtb7caW-l-UgHnh9ORATe5Ku_evvsvmZVI_6uCMI.svg%22%7D&auth_date=1732117099&signature=dUMV-_0Y-X96X7wcCy0CB5_ddeoH0-ZOjTObuKA26XDhdqS4TKGgGFb6qviJBXHPsT0R_v4y1e79-kVSKIkBDg&hash=43b9d3336c940d1f39d71e32f61ecb39b430ee2de887be1f3083ada3a84c68cb';
// Axios instance with default settings
export const api = axios.create({
    baseURL: API_BASE_URL,
    // headers: {
    //   Authorization: `${TOKEN}`, // Replace with your actual token
    //   'web-app-auth': `${TOKEN}`, // Optionally include other specific header
    // },
});
// Utility function to get Authorization token from storage (localStorage or sessionStorage, etc.)
const getAuthToken = () => {
    // Example: Assuming token is stored in localStorage
    return localStorage.getItem('token');
};
// Add Authorization header to axios instance
api.interceptors.request.use((config) => {
    const token = getAuthToken();
    //   if (token) {
    //     config.headers['Authorization'] = `${TOKEN}`;
    //   }
    return config;
});
// 1. **Login**
export const login = () => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const response = yield api.get('/login');
        return response.data;
    }
    catch (error) {
        console.error('Login failed:', error);
        throw error;
    }
});
// 2. **Get User**
export const getUser = () => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const response = yield api.get('/users');
        return response.data;
    }
    catch (error) {
        console.error('Failed to fetch user:', error);
        throw error;
    }
});
// 3. **Set User Address**
export const setUserAddress = (address) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const response = yield api.get(`/users/address/${address}`);
        return response.data;
    }
    catch (error) {
        console.error('Failed to set user address:', error);
        throw error;
    }
});
// 4. **Get Task by ID**
export const getTask = (taskId) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const response = yield api.get(`/tasks/${taskId}`);
        return response.data;
    }
    catch (error) {
        console.error('Failed to fetch task:', error);
        throw error;
    }
});
// 5. **Claim Task**
export const claimTask = (taskId) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const response = yield api.post(`/task/${taskId}/claim`);
        return response.data;
    }
    catch (error) {
        console.error('Failed to claim task:', error);
        throw error;
    }
});
// 6. **Complete Task**
export const completeTask = (taskId) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const response = yield api.get(`/tasks/${taskId}/complete`);
        return response.data;
    }
    catch (error) {
        console.error('Failed to complete task:', error);
        throw error;
    }
});
export const checkTask = (taskId) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const response = yield api.get(`/task/${taskId}/check`);
        return response.data;
    }
    catch (error) {
        console.error('Failed to check task:', error);
        throw error;
    }
});
// 7. **Get Categories**
export const getCategories = () => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const response = yield api.get('/categories');
        return response.data;
    }
    catch (error) {
        console.error('Failed to fetch categories:', error);
        throw error;
    }
});
export const getNft = () => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const response = yield api.get('/nft');
        return response.data;
    }
    catch (error) {
        console.error('Failed to fetch NFT:', error);
        throw error;
    }
});
// 8. **Get Category by ID**
export const getCategoryById = (categoryId) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const response = yield api.get(`/categories/${categoryId}`);
        return response.data;
    }
    catch (error) {
        console.error('Failed to fetch category:', error);
        throw error;
    }
});
// 9. **Get NFT by ID**
export const getNftById = (nftId) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const response = yield api.get(`/nfts/${nftId}`);
        return response.data;
    }
    catch (error) {
        console.error('Failed to fetch NFT:', error);
        throw error;
    }
});
// 10. **Get Branch by ID**
export const getBranchById = (branchId) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const response = yield api.get(`/branches/${branchId}`);
        return response.data;
    }
    catch (error) {
        console.error('Failed to fetch branch:', error);
        throw error;
    }
});
export const checkBranch = (branchId) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const response = yield api.get(`/branches/${branchId}/check`);
        return response.data;
    }
    catch (error) {
        console.error('Failed to check branch:', error);
        throw error;
    }
});
// 11. **Complete Branch**
export const completeBranch = (branchId) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const response = yield api.get(`/branches/${branchId}/complete`);
        return response.data;
    }
    catch (error) {
        console.error('Failed to complete branch:', error);
        throw error;
    }
});
//Claim peace
export const claimPiece = (pieceId) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const response = yield api.get(`/pieces/${pieceId}/claim`);
        return response.data;
    }
    catch (error) {
        console.error('Failed to claim piece:', error);
        throw error;
    }
});
// 12. **Reset Database**
export const resetDatabase = () => __awaiter(void 0, void 0, void 0, function* () {
    try {
        const response = yield api.get('/reset_database');
        return response.data;
    }
    catch (error) {
        console.error('Failed to reset database:', error);
        throw error;
    }
});
// You can create more API functions for other endpoints following the same pattern as above.
