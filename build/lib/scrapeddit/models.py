import torchvision
import torch
import torchvision.models as models

def get_efficient(device = False, freeze = False):
    weights = torchvision.models.EfficientNet_B0_Weights.DEFAULT
    if device == True: 
        if torch.backends.mps.is_available(): device = 'mps'
        else: device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model =  torchvision.models.efficientnet_b0(weights=weights).to(device)
    else: model = torchvision.models.efficientnet_b0(weights=weights)
    if freeze == True:
        for param in model.features.parameters():
            param.requires_grad = False
    return model

def get_vision_model(model_name='vgg16', pretrained=True, device=None, freeze = False):
    if device == True: 
        if torch.backends.mps.is_available(): device = 'mps'
        else: device = 'cuda' if torch.cuda.is_available() else 'cpu'
        model = models.__dict__[model_name](pretrained=pretrained).to(device)
    else: model = models.__dict__[model_name](pretrained=pretrained)
    if freeze == True:
        for param in model.features.parameters():
            param.requires_grad = False
    return model

