# Includes general Multimodal registration data structures for specific endpoints.
# Author: yqiao
import base64
from enum import Enum

from databind.core import ExtraKeys
from databind.core.dataclasses import dataclass
from sapiopylib.rest.pojo.DataRecord import DataRecord


@dataclass
class PySimpleMoleculePojo:
    imageSVG: str | None
    smiles: str
    molBlock: str


@dataclass
@ExtraKeys()
class PyMolecule:
    """
    Describes a deserialized molecule for Java.
    """
    imageSVG: str | None
    smiles: str
    clogP: float
    tpsa: float
    amw: float
    exactMass: float
    numHBondDonors: int
    numHBondAcceptors: int
    molFormula: str
    charge: int
    molBlock: str
    inchi: str
    inchiKey: str
    stereoisomers: list[PySimpleMoleculePojo] | None
    normError: str | None
    desaltError: str | None
    desaltedList: list[str] | None


@dataclass
class PyCompound:
    """
    class PyCompound
    """

    # The original substance data.
    originalMol: PyMolecule  # since May 24, 2023

    # The normalized, desalted abstract compound data.
    canonicalMol: PyMolecule | None  # since May 24, 2023

    props: dict[str, object] | None


@dataclass
class ChemDataType(Enum):
    CompoundPart = 'CompoundPart'
    ChemicalReagentPart = 'ChemicalReagentPart'

    def __init__(self, data_type_name: str):
        self._data_type_name = data_type_name

    @property
    def data_type_name(self):
        return self._data_type_name


class ChemFileType(Enum):
    CSV = 0
    SDF = 1


class ChemLoadType(Enum):
    SMILES_LIST = 0
    INCHI_LIST = 1
    MOL_BLOCK_LIST = 2
    SDF_FILE = 3


class ChemSearchType(Enum):
    """
    All possible chemistry quicksearch types.
    """
    COMPOUND_SUBSTRUCTURE = 0
    COMPOUND_SIMILARITY = 1
    REACTION_SUBSTRUCTURE = 2


@dataclass
class ChemLoadingError:
    """
    Describes a single record of compound loading error, this will be produced by interactive loader of compounds.
    Attributes:
        original: The original data that makes up the molecule so user can find it in the file.
        errorMsg: Why the import has failed. (normalization/desalting/sanitization/kekulize)
        properties: The additional attributes in the import. (for mols in SDF)
    """
    original: str
    errorMsg: str
    properties: dict


@dataclass
class PyMoleculeLoaderResult:
    """
    The results of a loading operation.

    Attributes:
        compoundByStr: may be blank if irrelevant. The map of source data string to the compound loaded.
        compoundList: the compounds successfully loaded.
        errorList: an error record is added here for each one we failed to load in Sapio.
    """
    compoundByStr: dict[str, PyCompound]
    compoundList: list[PyCompound]
    errorList: list[ChemLoadingError]


@dataclass
class ChemCompleteImportPojo:
    # Variables declaration with type hints
    dataTypeName: str
    successPartRecordIdList: list[int] | None
    successSampleRecordIdList: list[int] | None
    errors: list[ChemLoadingError] | None
    registeredOriginalParts: list[int]
    allRegisteredPartsNoDuplicates: list[int]
    newPartList: list[int]
    numOldParts: int


@dataclass
class ChemInteractiveRegisterRequestPojo:
    dataType: ChemDataType
    fileType: ChemFileType
    fileDataEncodedBase64: str | None
    addingItems: bool

    def __init__(self, data_type: ChemDataType, file_type: ChemFileType, is_adding_items: bool, file_data: bytes):
        self.dataType = data_type
        self.fileType = file_type
        self.addingItems = is_adding_items
        self.fileDataEncodedBase64 = base64.b64encode(file_data).decode()


@dataclass
class CompoundLoadRequestPojo:
    """
    Describes a load request for the Load Compound Endpoint.

    Attributes:
        dataType: The data type of records to be registered in Sapio.
        loadType: The source data's type you are loading.
        dataList: If the source data is not a file, here you specify a list of string describing molecule for that src.
        fileDataBase64: If the source data is a file, the file's base64 data content.
    """
    dataType: ChemDataType
    loadType: ChemLoadType
    dataList: list[str] | None
    fileDataBase64: str | None

    def __init__(self, data_type: ChemDataType, load_type: ChemLoadType, data_list: list[str] | None = None,
                 file_data: bytes | None = None):
        self.dataType = data_type
        self.loadType = load_type
        if load_type is ChemLoadType.SDF_FILE:
            self.dataList = None
            if file_data is None:
                raise ValueError("The file data must be specify the the load type is of a file type.")
            self.fileDataBase64 = base64.b64encode(file_data).decode()
        else:
            self.dataList = data_list
            self.fileDataBase64 = None


@dataclass
class ChemRegisterRequestPojo:
    """
    Data payload to send to webservice to request registration in RegisterCompoundEndpoint

    Attributes:
        dataType: The data type of records to be registered in Sapio.
        registrationList: This list must be of correct data structure suitable for the type. For example, for CompoundPart data type the canonical form must be resolved by earlier call.
    """
    dataType: ChemDataType
    registrationList: list[PyCompound]

    def __init__(self, data_type: ChemDataType, registration_list: list[PyCompound]):
        self.dataType = data_type
        self.registrationList = registration_list


@dataclass
class ImageDataRequestPojo:
    """
    Payload to request in endpoint loading of image data of a compound or a reaction in Sapio's unified drawing format.

    Attributes:
        dataList: The list of data about the images of the molecules or reactions. This can be SMILES, MOL, or INCHI. SMILES is expected. INCHI can be ambiguous to chrality as well as tautomers.
        isReaction: true if the underlying data is of RxN format of reaction.
    """
    dataList: list[str]
    reaction: bool

    def __init__(self, data_list: list[str], is_reaction: bool):
        self.dataList = data_list
        self.reaction = is_reaction


@dataclass
class PyIndigoReactionPojo:
    """
    The result of loading a reaction.

    Attributes:
        products: products of the reaction.
        reactants: reactants of the reaction.
        reactionSmiles: the SMILES representation of this reaction.
        reactionRxn: the RxN of an arotmized reaction
        reactionRenderRxn: the RxN of no-automapping, DE-aromotized reaction, with 2D coordinates of atoms computed.
    """
    products: list[PyCompound]
    reactants: list[PyCompound]
    reactionSmiles: str
    reactionRxn: str
    reactionRenderRxn: str


class CartridgeMolJoinMethod(Enum):
    """
    The structure search join method to filter results against Sapio registry.
    Since we have multiple registries in Sapio, you will need to specify which one to join against.
    """
    COMPOUND_REGISTRY = 0
    REAGENT_REGISTRY = 1
    HELM_STRUCTURE = 2


@dataclass
class ChemQuickSearchContextData:
    """
    Do not directly make use of this class. The only use for this class is to pass in the "next page"
    produced by the endpoint.

    When obtaining the first page, this parameter argument should not be passed at all (not created with default values).
    """
    previousPageSearchAfterJsonStack: list[str] | None
    nextPageSearchAfter: str | None
    pitId: str | None
    query: str | None
    joinMethod: CartridgeMolJoinMethod | None
    simUpperLimit: float | None


@dataclass
class ChemSearchRequestPojo:
    """
    Payload to send to endpoint to request a chemical search in Sapio.
    This can be a substructure search or similarity search.

    Attributes:
        searchStr: The search string of SMILES or SMARTS you are searching
        searchType: The type of search you are doing.
        joinMethod: The registry you are using to join with Sapio record. This is not relevant for reactions.
        contextData: The context data of the current page passed to you by result of previous page. If this is the first page you are querying, leave this as None.
        simSearchUpperLimit: similarity search upper limit, between 0.0 to 1.0, valid only to similarity searches.
    """
    searchStr: str
    searchType: ChemSearchType
    joinMethod: CartridgeMolJoinMethod | None
    contextData: ChemQuickSearchContextData | None
    simSearchUpperLimit: float | None

    def __init__(self, search_str: str, search_type: ChemSearchType, join_method: CartridgeMolJoinMethod | None = None,
                 context_data: ChemQuickSearchContextData | None = None, sim_search_upper: float | None = None):
        self.searchStr = search_str
        self.searchType = search_type
        self.joinMethod = join_method
        self.contextData = context_data
        self.simSearchUpperLimit = sim_search_upper


@dataclass
class ChemSearchResponsePojo:
    """
    A response object of a chemistry quick search.
    NOTE: It's possible to have next page while the current records list is blank (although without additional query conditions, this should be rare).

    Attributes:
         recordsOfPage: The records returned in this page.
         nextPageAvailable: Whether there is still a next page to query. If this is filled, then the context to query next page is on nextPageContext.

    """
    recordIdListOfPage: list[int]
    nextPageAvailable: bool
    nextPageContext: ChemQuickSearchContextData


