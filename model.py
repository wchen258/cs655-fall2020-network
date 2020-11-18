from torchvision import models
from torchvision import transforms
from PIL import Image
import torch
import ast
import sys


if __name__=='__main__':
	alexnet = models.alexnet(pretrained=True)
	transform = transforms.Compose([           
 		transforms.Resize(256),                   
 		transforms.CenterCrop(224),                
 		transforms.ToTensor(),                    
 		transforms.Normalize(                    
 		mean=[0.485, 0.456, 0.406],                
		std=[0.229, 0.224, 0.225]                  
		)])

	img = Image.open(sys.argv[1])
	img_t = transform(img)
	batch_t = torch.unsqueeze(img_t, 0)
	alexnet.eval()
	out = alexnet(batch_t)

	with open("ImageNet_labels.txt", "r") as f:
		contents = f.read()
		dictionary = ast.literal_eval(contents)
	
	_, index = torch.max(out, 1)
	percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
	print(dictionary[index[0].item()], percentage[index[0]].item())	
