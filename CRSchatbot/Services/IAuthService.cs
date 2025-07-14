using CRSchatbotAPI.DTO;
using CRSchatbotAPI.Models;

namespace CRSchatbotAPI.Services
{
    public interface IAuthService
    {
        Task<string> LoginAsync(UserDto request);
        Task<User?> RegisterAsync(UserDto request);
    }
}