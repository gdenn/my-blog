{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 20,
   "id": "eced0ee2",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "INFO:root:__set__: '2.2.2.2'\n"
     ]
    },
    {
     "ename": "ValidationException",
     "evalue": "5.5.5. is not a valid ipv4 address",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mValidationException\u001b[0m                       Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-20-4a9ac08ac09c>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[1;32m     50\u001b[0m \u001b[0mflow\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mFlow\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     51\u001b[0m \u001b[0mflow\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0msrc_ipv4\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;34m\"2.2.2.2\"\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 52\u001b[0;31m \u001b[0mflow\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mdst_ipv4\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0;34m\"5.5.5.\"\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[0;32m<ipython-input-20-4a9ac08ac09c>\u001b[0m in \u001b[0;36m__set__\u001b[0;34m(self, obj, value)\u001b[0m\n\u001b[1;32m     20\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     21\u001b[0m     \u001b[0;32mdef\u001b[0m \u001b[0m__set__\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mself\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mobj\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mvalue\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 22\u001b[0;31m         \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mvalidate\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mvalue\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     23\u001b[0m         \u001b[0mlogging\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0minfo\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"__set__: %r\"\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mvalue\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     24\u001b[0m         \u001b[0msetattr\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mobj\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mself\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mproperty_name\u001b[0m\u001b[0;34m,\u001b[0m \u001b[0mvalue\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;32m<ipython-input-20-4a9ac08ac09c>\u001b[0m in \u001b[0;36mvalidate\u001b[0;34m(self, value)\u001b[0m\n\u001b[1;32m     38\u001b[0m         \u001b[0mipv4_pattern\u001b[0m \u001b[0;34m=\u001b[0m \u001b[0mre\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mcompile\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34mr'^(?:[0-9]{1,3}\\.){3}[0-9]{1,3}$'\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     39\u001b[0m         \u001b[0;32mif\u001b[0m \u001b[0;32mnot\u001b[0m \u001b[0mipv4_pattern\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mmatch\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mvalue\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m:\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m---> 40\u001b[0;31m             \u001b[0;32mraise\u001b[0m \u001b[0mValidationException\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m\"{} is not a valid ipv4 address\"\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mformat\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0mvalue\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m     41\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m     42\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
      "\u001b[0;31mValidationException\u001b[0m: 5.5.5. is not a valid ipv4 address"
     ]
    }
   ],
   "source": [
    "import logging\n",
    "import re\n",
    "from abc import ABC, abstractmethod\n",
    "\n",
    "logging.basicConfig(level=logging.INFO)\n",
    "\n",
    "\n",
    "class ValidationException(Exception):\n",
    "    pass\n",
    "\n",
    "class PropertyWithValidator(ABC):\n",
    "\n",
    "    def __set_name__(self, owner, name):\n",
    "        self.property_name = \"_\" + name\n",
    "        \n",
    "    def __get__(self, obj, obj_type=None):\n",
    "        value = getattr(obj, self.property_name)\n",
    "        logging.info(\"__get__: %r\", value)\n",
    "        return value\n",
    "        \n",
    "    def __set__(self, obj, value):\n",
    "        self.validate(value)\n",
    "        logging.info(\"__set__: %r\", value)\n",
    "        setattr(obj, self.property_name, value)\n",
    "\n",
    "    @abstractmethod\n",
    "    def validate(self, value):\n",
    "        pass\n",
    "    \n",
    "    \n",
    "class IPv4(PropertyWithValidator):\n",
    "    \n",
    "    def validate(self, value):\n",
    "        \n",
    "        if type(value) is not str:\n",
    "            raise ValidationException(\"{} must be a string to be a valid ipv4 address\".format(value))\n",
    "        \n",
    "        ipv4_pattern = re.compile(r'^(?:[0-9]{1,3}\\.){3}[0-9]{1,3}$')\n",
    "        if not ipv4_pattern.match(value):\n",
    "            raise ValidationException(\"{} is not a valid ipv4 address\".format(value))\n",
    "    \n",
    "class Flow:\n",
    "    \n",
    "    src_ipv4 = IPv4()\n",
    "    dst_ipv4 = IPv4()\n",
    "\n",
    "    \n",
    "flow = Flow()\n",
    "flow.src_ipv4 = \"2.2.2.2\"\n",
    "flow.dst_ipv4 = \"5.5.5.\""
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "fc25871e",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.5"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
