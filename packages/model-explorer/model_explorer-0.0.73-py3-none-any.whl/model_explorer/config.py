import json
import os
from typing import Any, Callable, Tuple, TypedDict, Union
from urllib.parse import quote

import torch
from typing_extensions import NotRequired

from .pytorch_exported_program_adater_impl import \
    PytorchExportedProgramAdapterImpl
from .types import ModelExplorerGraphs

ModelSource = TypedDict(
    'ModelSource', {'url': str, 'adapterId': NotRequired[str]})
EncodedUrlData = TypedDict('EncodedUrlData', {'models': list[ModelSource]})


class ModelExplorerConfig:
  """Stores the data to be visualized in Model Explorer."""

  def __init__(self) -> None:
    self.model_sources: list[ModelSource] = []
    self.graphs_list: list[ModelExplorerGraphs] = []

  def add_model_from_path(self, path: str, adapterId: str = '') -> 'ModelExplorerConfig':
    """Adds a model path to the config.

    Args:
      path: the model path to add.
      adapterId: the id of the adapter to use. Default is empty string meaning
          it will use the default adapter.
    """
    # Get the absolute path (after expanding home dir path "~").
    abs_model_path = os.path.abspath(os.path.expanduser(path))

    # Construct model source and add it.
    model_source: ModelSource = {'url': abs_model_path}
    if adapterId != '':
      model_source['adapterId'] = adapterId
    self.model_sources.append(model_source)

    return self

  def add_model_from_pytorch(self, model: Callable, inputs: Tuple[Any, ...]) -> 'ModelExplorerConfig':
    """Adds the given pytorch model.

    Args:
      model: The callable to trace.
      inputs: Example positional inputs.
    """
    # Convert the given model to model explorer graphs.
    print('Converting pytorch model to model explorer graphs...')
    exported = torch.export.export(model, inputs)
    adapter = PytorchExportedProgramAdapterImpl(exported)
    graphs = adapter.convert()
    graphs_index = len(self.graphs_list)
    self.graphs_list.append(graphs)

    # Construct model source.
    #
    # The model source has a special format, in the form of:
    # graphs://{src_model_type}/{graphs_index}
    model_source: ModelSource = {'url': f'graphs://pytorch/{graphs_index}'}
    self.model_sources.append(model_source)

    return self

  def to_url_param_value(self) -> str:
    """Converrts the config to the url param value."""
    # Construct url data.
    encoded_url_data: EncodedUrlData = {
        'models': self.model_sources
    }

    # Return its json string.
    return quote(json.dumps(encoded_url_data))

  def get_model_explorer_graphs(self, index: int) -> ModelExplorerGraphs:
    return self.graphs_list[index]

  def has_models(self) -> bool:
    return len(self.model_sources) > 0
