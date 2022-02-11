


class AlexNet(nn.Module):
    def __init__(self):
        super(AlexNet, self).__init__()

        self.cnn = nn.Sequential(
            # 卷积层1，3通道输入，96个卷积核，核大小11*11，步长4，填充2
            # 经过该层图像大小变为224-11+2*2 / 2 +1，55*55
            # 经3*3最大池化，2步长，图像变为55-3 / 2 + 1， 27*27
            nn.Conv2d(3, 96, 11, 4, 2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, 2, 0),
            #             nn.BatchNorm2d(96),

            # 卷积层2，96输入通道，256个卷积核，核大小5*5，步长1，填充2
            # 经过该层图像变为27-5+2*2 / 1 + 1，27*27
            # 经3*3最大池化，2步长，图像变为27-3 / 2 + 1， 13*13
            nn.Conv2d(96, 256, 5, 1, 2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(3, 2, 0),
            #             nn.BatchNorm2d(256),

            # 卷积层3，256输入通道，384个卷积核，核大小3*3，步长1，填充1
            # 经过该层图像变为3-3+2*1 / 1 + 1，13*13
            nn.Conv2d(256, 384, 3, 1, 1),
            nn.ReLU(inplace=True),

            # 卷积层4，384输入通道，384个卷积核，核大小3*3，步长1，填充1
            # 经过该层图像变为3-3+2*1 / 1 + 1，13*13
            nn.Conv2d(384, 384, 3, 1, 1),
            nn.ReLU(inplace=True),

            # 卷积层5，384输入通道，256个卷积核，核大小3*3，步长1，填充1
            # 经过该层图像变为3-3+2*1 / 1 + 1，13*13
            nn.Conv2d(384, 256, 3, 1, 1),
            nn.ReLU(inplace=True),

            # 最后一层池化，图像变为256 * 6 * 6
            nn.MaxPool2d(3, 2, 0)
        )

        self.fc = nn.Sequential(
            # 256个feature，每个feature 3*3
            nn.Linear(256*6*6, 1024),
            nn.Dropout(p=0.5),
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.Dropout(p=0.5),
            nn.ReLU(),
            nn.Linear(512, 1)
        )

    def forward(self, x):
        x = self.cnn(x)

        # x.size()[0]: batch size
        x = x.view(x.size()[0], -1)
        x = self.fc(x)

        return x


class VGG(nn.Module):
    def __init__(self, arch, num_classes=1):
        self.in_channels = 3
        super().__init__()
        self.conv3_64 = self.__make_layers(64, arch[0])
        self.conv3_128 = self.__make_layers(128, arch[1])
        self.conv3_256 = self.__make_layers(256, arch[2])
        self.conv3_512a = self.__make_layers(512, arch[3])
        self.conv3_512b = self.__make_layers(512, arch[4])

        self.fcc = nn.Sequential(
            nn.Linear(7 * 7 * 512, 4096),
            nn.ReLU(),
            nn.Linear(4096, 512),
            nn.ReLU(),
            nn.Linear(512, num_classes)
        )

    def forward(self, x):
        # conv layers
        x = self.conv3_64(x)  # out: 112 x 112
        x = self.conv3_128(x)  # out: 56 x 56
        x = self.conv3_256(x)  # out: 28 x 28
        x = self.conv3_512a(x)  # out: 14 x 14
        x = self.conv3_512b(x)  # out: 7 x 7
        x = x.view(x.size()[0], -1)

        # fcc layers
        out = self.fcc(x)
        return out

    def __make_layers(self, channels, num):
        vggBlock = []
        for i in range(num):
            vggBlock.append(nn.Conv2d(self.in_channels, channels, 3, 1, 1))
            vggBlock.append(nn.ReLU())
            vggBlock.append(nn.BatchNorm2d(channels))
            self.in_channels = channels
        vggBlock.append(nn.MaxPool2d(2, 2))
        return nn.Sequential(*vggBlock)


def VGG_11():
    return VGG([1, 1, 2, 2, 2], num_classes=1)


def VGG_13():
    return VGG([2, 2, 2, 2, 2], num_classes=1)


def VGG_16():
    return VGG([2, 2, 3, 3, 3], num_classes=1)


def VGG_19():
    return VGG([2, 2, 4, 4, 4], num_classes=1)

############### classes for ResNet #############


class BN_Conv2d(nn.Module):
    """
    BN_CONV, default activation is ReLU
    """

    def __init__(self, in_channels: object, out_channels: object, kernel_size: object, stride: object, padding: object,
                 dilation=1, groups=1, bias=False, activation=True) -> object:
        super(BN_Conv2d, self).__init__()
        layers = [nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size, stride=stride,
                            padding=padding, dilation=dilation, groups=groups, bias=bias),
                  nn.BatchNorm2d(out_channels)]
        if activation:
            layers.append(nn.ReLU(inplace=True))
        self.seq = nn.Sequential(*layers)

    def forward(self, x):
        return self.seq(x)


class BasicBlock(nn.Module):
    """
    basic building block for ResNet-18, ResNet-34
    """
    message = "basic"

    def __init__(self, in_channels, out_channels, strides):
        super(BasicBlock, self).__init__()
        self.conv1 = BN_Conv2d(in_channels, out_channels, 3,
                               stride=strides, padding=1, bias=False)  # same padding
        self.conv2 = BN_Conv2d(out_channels, out_channels, 3,
                               stride=1, padding=1, bias=False, activation=False)

        # fit input with residual output
        self.short_cut = nn.Sequential()
        if strides is not 1:
            self.short_cut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, 1,
                          stride=strides, padding=0, bias=False),
                nn.BatchNorm2d(out_channels)
            )

    def forward(self, x):
        out = self.conv1(x)
        out = self.conv2(out)
        out = out + self.short_cut(x)
        return F.relu(out)


class BottleNeck(nn.Module):
    """
    BottleNeck block for RestNet-50, ResNet-101, ResNet-152
    """
    message = "bottleneck"

    def __init__(self, in_channels, out_channels, strides):
        super(BottleNeck, self).__init__()
        self.conv1 = BN_Conv2d(in_channels, out_channels, 1,
                               stride=1, padding=0, bias=False)  # same padding
        self.conv2 = BN_Conv2d(out_channels, out_channels,
                               3, stride=strides, padding=1, bias=False)
        self.conv3 = BN_Conv2d(out_channels, out_channels * 4,
                               1, stride=1, padding=0, bias=False, activation=False)

        # fit input with residual output
        self.shortcut = nn.Sequential(
            nn.Conv2d(in_channels, out_channels * 4, 1,
                      stride=strides, padding=0, bias=False),
            nn.BatchNorm2d(out_channels * 4)
        )

    def forward(self, x):
        out = self.conv1(x)
        out = self.conv2(out)
        out = self.conv3(out)
        out = out + self.shortcut(x)
        return F.relu(out)


class ResNet(nn.Module):
    """
    building ResNet_34
    """

    def __init__(self, block: object, groups: object, num_classes=1) -> object:
        super(ResNet, self).__init__()
        self.channels = 64  # out channels from the first convolutional layer
        self.block = block

        self.conv1 = nn.Conv2d(3, self.channels, 7,
                               stride=2, padding=3, bias=False)
        self.bn = nn.BatchNorm2d(self.channels)
        self.pool1 = nn.MaxPool2d(3, 2, 1)
        self.conv2_x = self._make_conv_x(
            channels=64, blocks=groups[0], strides=1, index=2)
        self.conv3_x = self._make_conv_x(
            channels=128, blocks=groups[1], strides=2, index=3)
        self.conv4_x = self._make_conv_x(
            channels=256, blocks=groups[2], strides=2, index=4)
        self.conv5_x = self._make_conv_x(
            channels=512, blocks=groups[3], strides=2, index=5)
        self.pool2 = nn.AvgPool2d(7)
        patches = 512 if self.block.message == "basic" else 512 * 4
        self.fc = nn.Linear(patches, num_classes)  # for 224 * 224 input size

    def _make_conv_x(self, channels, blocks, strides, index):
        """
        making convolutional group
        :param channels: output channels of the conv-group
        :param blocks: number of blocks in the conv-group
        :param strides: strides
        :return: conv-group
        """
        list_strides = [strides] + [1] * (blocks -
                                          1)  # In conv_x groups, the first strides is 2, the others are ones.
        conv_x = nn.Sequential()
        for i in range(len(list_strides)):
            # when use add_module, the name should be difference.
            layer_name = str("block_%d_%d" % (index, i))
            conv_x.add_module(layer_name, self.block(
                self.channels, channels, list_strides[i]))
            self.channels = channels if self.block.message == "basic" else channels * 4
        return conv_x

    def forward(self, x):
        out = self.conv1(x)
        out = F.relu(self.bn(out))
        out = self.pool1(out)
        out = self.conv2_x(out)
        out = self.conv3_x(out)
        out = self.conv4_x(out)
        out = self.conv5_x(out)
        out = self.pool2(out)
        out = out.view(out.size(0), -1)
        out = self.fc(out)
        return out


def ResNet_18(num_classes=1):
    return ResNet(block=BasicBlock, groups=[2, 2, 2, 2], num_classes=num_classes)


def ResNet_34(num_classes=1):
    return ResNet(block=BasicBlock, groups=[3, 4, 6, 3], num_classes=num_classes)


def ResNet_50(num_classes=1):
    return ResNet(block=BottleNeck, groups=[3, 4, 6, 3], num_classes=num_classes)


def ResNet_101(num_classes=1):
    return ResNet(block=BottleNeck, groups=[3, 4, 23, 3], num_classes=num_classes)


def ResNet_152(num_classes=1):
    return ResNet(block=BottleNeck, groups=[3, 8, 36, 3], num_classes=num_classes)
