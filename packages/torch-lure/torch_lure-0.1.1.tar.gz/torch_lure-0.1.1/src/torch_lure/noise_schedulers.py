import torch
from torch import nn


class LinearNoiseSchedule(nn.Module):
    def __init__(self, beta_start=1e-4, beta_end=0.02, num_timesteps=1000):
        super().__init__()
        self.num_timesteps = num_timesteps

        betas = torch.linspace(beta_start, beta_end, num_timesteps)
        alphas = 1 - betas
        alphas_cumprod = torch.cumprod(alphas, dim=0)

        self.register_buffer("betas", betas)
        self.register_buffer("alphas", alphas)
        self.register_buffer("alphas_cumprod", alphas_cumprod)

    def get_alpha(self, t):
        return self.alphas[t]

    def get_variance(self, t):
        return 1 - self.alphas[t]

    def get_previous_alpha(self, t):
        return self.alphas_cumprod[t - 1] if t > 0 else 1

    def sample_noise(self, x_0, t):
        noise = torch.randn_like(x_0)
        sqrt_alpha_cumprod = torch.sqrt(self.alphas_cumprod[t])
        sqrt_one_minus_alpha_cumprod = torch.sqrt(1 - self.alphas_cumprod[t])
        return sqrt_alpha_cumprod * x_0 + sqrt_one_minus_alpha_cumprod * noise

    def sample_noise_from_output(self, x_0, t, noise_pred):
        sqrt_one_minus_alpha_cumprod = torch.sqrt(1 - self.alphas_cumprod[t])
        return x_0 - sqrt_one_minus_alpha_cumprod * noise_pred


class CosineNoiseSchedule(nn.Module):
    def __init__(self, max_beta=0.999, noise_cosine_shift=0.008, num_timesteps=1000):
        super().__init__()
        self.num_timesteps = num_timesteps

        timesteps = torch.arange(1, num_timesteps + 1, dtype=torch.float64)
        alphas_cumprod = self._cosine_variance_schedule(timesteps / num_timesteps)
        betas = 1 - alphas_cumprod[1:] / alphas_cumprod[:-1]

        self.register_buffer("betas", betas)
        self.register_buffer("alphas_cumprod", alphas_cumprod)
        self.noise_cosine_shift = noise_cosine_shift
        self.max_beta = max_beta

    def get_alpha(self, t):
        return self.alphas_cumprod[t + 1] / self.alphas_cumprod[t]

    def get_variance(self, t):
        return self.betas[t]

    def get_previous_alpha(self, t):
        return self.alphas_cumprod[t - 1] if t > 0 else 1

    def sample_noise(self, x_0, t):
        noise = torch.randn_like(x_0)
        sqrt_alpha_cumprod = torch.sqrt(self.alphas_cumprod[t])
        sqrt_one_minus_alpha_cumprod = torch.sqrt(1 - self.alphas_cumprod[t])
        return sqrt_alpha_cumprod * x_0 + sqrt_one_minus_alpha_cumprod * noise

    def sample_noise_from_output(self, x_0, t, noise_pred):
        sqrt_one_minus_alpha_cumprod = torch.sqrt(1 - self.alphas_cumprod[t])
        return x_0 - sqrt_one_minus_alpha_cumprod * noise_pred

    def _cosine_variance_schedule(self, t):
        s = self.noise_cosine_shift
        max_beta = self.max_beta
        f_t = torch.cos((t + s) / (1 + s) * torch.pi / 2) ** 2
        f_0 = torch.cos(s / (1 + s) * torch.pi / 2) ** 2
        return f_0 - (f_0 - max_beta) * (f_t / f_0)
