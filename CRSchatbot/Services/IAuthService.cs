using CRSchatbot.Shared.DTO;
using CRSchatbotAPI.DTO;
using CRSchatbotAPI.Models;

namespace CRSchatbotAPI.Services
{
    public interface IAuthService
    {
        Task<LoginResponseDto> LoginAsync(UserDto request); 
        Task<User?> RegisterAsync(UserDto request);
    }
}