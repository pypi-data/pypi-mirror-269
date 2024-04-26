import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from tqdm import tqdm

# Device configuration
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Hyperparameters
latent_size = 100
hidden_size = 256
image_size = 50
num_epochs = 50
batch_size = 64
learning_rate = 0.0002

# Define Generator network
class Generator(nn.Module):
    def __init__(self):
        super(Generator, self).__init__()
        self.main = nn.Sequential(
            nn.Linear(latent_size, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, hidden_size * 2),
            nn.ReLU(),
            nn.Linear(hidden_size * 2, image_size * image_size),
            nn.Tanh()  # Output image in range [-1, 1]
        )

    def forward(self, x):
        return self.main(x).view(-1, 1, image_size, image_size)

# Define Discriminator network
class Discriminator(nn.Module):
    def __init__(self):
        super(Discriminator, self).__init__()
        self.main = nn.Sequential(
            nn.Linear(image_size * image_size, hidden_size * 2),
            nn.ReLU(),
            nn.Linear(hidden_size * 2, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1),
            nn.Sigmoid()  # Output probability of real/fake
        )

    def forward(self, x):
        x = x.view(-1, image_size * image_size)
        return self.main(x)


def _train(self):
    # Initialize networks
    generator = Generator().to(device)
    discriminator = Discriminator().to(device)

    # Define loss function and optimizers
    criterion = nn.BCELoss()
    gen_optimizer = optim.Adam(generator.parameters(), lr=learning_rate, betas=(0.5, 0.999))
    disc_optimizer = optim.Adam(discriminator.parameters(), lr=learning_rate, betas=(0.5, 0.999))

    # Data loading
    transform = transforms.Compose([
        transforms.Resize(image_size),
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])
    dataset = datasets.MNIST(root='./data', train=True, transform=transform, download=True)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

    # Training loop
    for epoch in range(num_epochs):
        for i, (real_images, _) in enumerate(tqdm(dataloader)):
            real_images = real_images.to(device)
            real_labels = torch.ones(batch_size, 1).to(device)
            fake_labels = torch.zeros(batch_size, 1).to(device)

            # Train Discriminator
            discriminator.zero_grad()
            outputs_real = discriminator(real_images)
            d_loss_real = criterion(outputs_real, real_labels)
            d_loss_real.backward()

            z = torch.randn(batch_size, latent_size).to(device)
            fake_images = generator(z)
            outputs_fake = discriminator(fake_images.detach())
            d_loss_fake = criterion(outputs_fake, fake_labels)
            d_loss_fake.backward()
            disc_optimizer.step()

            # Train Generator
            generator.zero_grad()
            outputs = discriminator(fake_images)
            g_loss = criterion(outputs, real_labels)
            g_loss.backward()
            gen_optimizer.step()

            # Print losses
            if (i+1) % 100 == 0:
                print(f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{len(dataloader)}], '
                      f'D_loss: {d_loss_real.item()+d_loss_fake.item():.4f}, '
                      f'G_loss: {g_loss.item():.4f}')

    # Save the trained model
    torch.save(generator.state_dict(), 'generator.pth')
